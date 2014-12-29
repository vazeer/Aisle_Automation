#!/usr/bin/env python
#

"""Implementation of VUE Backend REST API.

DOC: <Insert internal doc link here>
"""

__author__ = 'drno@thesilverlabs.com (Dr. No)'


import webapp2
import time
import json
import logging
import base64
import datetime
from google.appengine.ext import db


# Hardcoded User key id for testing purposes. Assign it to None to disable.
_USER_KEY_ID = None


# TODO: This codes needs major refactoring. For easy of development, all the
# classes are being clubbed in single file.

# TODO: Make all response strings to unicode. Put some thought around
# multi-language support

# Note: All the entity fields are converted to Json at some point. Hence the
# attribute (field) naming is created in line with JavaScript
# TODO: Add verbose_name to all fields 
class Aisle(db.Model):
  # TODO: Weigh the benefit of storing user_key_id vs the dynamic query
  # implemented in user() method below
  #user_key_id = db.IntegerProperty(required=True)
  name = db.StringProperty()
  lookingFor = db.StringProperty(required=True)
  category = db.StringProperty(required=True)
  occasion = db.StringProperty(required=True)
  findItAt = db.StringProperty()
  # Note: RefImageId should be required, but because it cant be set until images
  # are saved first, makeing is not a required field.
  refImageId = db.IntegerProperty()
  
  @property
  def user(self):
    return AisleList.all().filter('aisles', self.key()).get().parent()


# TODO: Add verbose_name to all fields
# TODO: Add Current, expired, drafts, bookmarks, recently viewed
# NOTE: AisleList 
class AisleList(db.Model):
  aisles = db.ListProperty(db.Key)


# TODO: Add verbose_name to all fields 
class User(db.Model):
  firstName = db.StringProperty()
  lastName = db.StringProperty()
  joinTime = db.IntegerProperty(
      verbose_name='User join time in UTC msec')
  email = db.EmailProperty()
  

# TODO: Add verbose_name to all fields 
class Image(db.Model):
  title = db.StringProperty()
  imageUrl = db.StringProperty()
  detailsUrl = db.LinkProperty()
  store = db.StringProperty()
  height = db.IntegerProperty()
  width = db.IntegerProperty()
  ownerAisleId = db.IntegerProperty()
  ownerUserId = db.IntegerProperty()
  
  @property
  def aisles(self):
    "Returns all the aisles that have this image."
    return ImageList.all().filter('images', self.key()).run()
  
  @property
  def users(self):
    "Returns all the users that have this image."
    for image_list in self.aisles:
      yield image_list.parent().user

# TODO: Add verbose_name to all fields 
class ImageList(db.Model):
  images = db.ListProperty(db.Key)


# TODO: authenticator module needs redesign
AUTHENTICATE_HEADER = "WWW-Authenticate"
AUTHORIZATION_HEADER = "Authorization"
AUTHENTICATE_TYPE = 'Basic realm="Secure Area"'
CONTENT_TYPE_HEADER = "Content-Type"
HTML_CONTENT_TYPE = "text/html"

class Authenticator():

  def __init__(self):
    pass

  def authenticate(self, dispatcher):
    # Parse the header to extract a user/password combo.
    # We're expecting something like "Basic XZxgZRTpbjpvcGVuIHYlc4FkZQ=="
    try:
      auth_header = dispatcher.request.headers[AUTHORIZATION_HEADER]
    except KeyError:
      # set the headers requesting the browser to prompt for a user/password:
      dispatcher.response.set_status(401, message="Authentication Required")
      dispatcher.response.headers[AUTHENTICATE_HEADER] = AUTHENTICATE_TYPE
      dispatcher.response.headers[CONTENT_TYPE_HEADER] = HTML_CONTENT_TYPE
  
      dispatcher.response.out.write(
          '<html><body>401 Authentication Required</body></html>')
      return

    # Isolate the encoded user/passwd and decode it
    auth_parts = auth_header.split(' ')
    user_pass_parts = base64.b64decode(auth_parts[1]).split(':')
    user_arg = user_pass_parts[0]
    pass_arg = user_pass_parts[1]
    logging.info('User= %s, pass=%s', user_arg, pass_arg)


# TODO: Authorizer module needs implementation
class Authorizer():
  pass

# TODO: Investigate if it makes sense to deliver user error messages from
# backend. 
class ApiHandlerException(Exception):
  """Exceptions from Api Handler."""
  def __init__(self, err_code, err_msg=None, detailed_err_msg=None):
    """ Initialize ApiHandelerException object.
    
    Args:
      error_code: Integer code of the error occured. Usually HTTP code.
      err_msg: One line error message.
      detailed_err_msg: Multi lined error message.
    """
    super(ApiHandlerException, self).__init__()
    self.err_code = err_code
    self.err_msg = err_msg
    self.detailed_err_msg = detailed_err_msg

  def ToDict(self):
    """Returns the exception codes and messages as a dict.
    
    Returns:
      A Dict containing error details.
    """
    error_dict = {}
    if self.err_code is not None:
      error_dict['code'] = self.err_code
    if self.err_msg is not None:
      error_dict['msg'] = self.err_msg
    if self.detailed_err_msg is not None:
      error_dict['detailed_msg'] = self.detailed_err_msg
    return error_dict
  
  def ToJson(self):
    """Returns the exception codes and messages as a json string.
    
    Returns:
      A json string containing error details.
    """
    return json.dumps(self.ToDict())
 

# TODO: Implement stricter Content-type and Accept encoding checking
class ApiHandler(webapp2.RequestHandler):
  
  def __init__(self, *args, **kwargs):
    super(ApiHandler, self).__init__(*args, **kwargs)
    
    # TODO: Implement Authentication and Authorization layer here

    # Note: These are commented out for easy of testing
    #content_type = self.request.headers.get('Content-Type')
    #if (content_type is None or
    #    content_type != 'application/json'):
    #  logging.error('Request has incompatible content-type: %s',
    #                content_type)
    #  raise ApiHandlerException(400)
    
    path_split = self.request.path.strip('/').split('?')[0].split('/')
    if len(path_split) < 3:
      logging.error('Invalid url: %s. URL should at minimum '
                    'contain /rest/<version>/<model>/...', self.request.url)
      raise ApiHandlerException(400)
    
    # Model is the Datastore Entity
    self._model = path_split[2]
    # Model args are the arguments passed to Model's Rest API.
    self._model_args = path_split[3:]

    # These variables are set by methods down below
    self._user_parent_key = None
    self._user = None
    self._user_aisle_list = None
    self._payload = None
    
  def GetPayload(self):
    """Returns self._payload variable. Builds it from request.body if necessary.
    
    Returns:
      Returns self._payload
    """
    if self._payload is None:
      if self.request.body:
        content_type = self.request.headers.get('Content-Type')
        if (content_type is None or
            content_type != 'application/json'):
          logging.error('Content-Type header is set to: %s. '
                        'Expecting "application/json"', content_type)
          raise ApiHandlerException(400)
        try:
          self._payload = json.loads(self.request.body)
        except ValueError as e:
          logging.error('Cant understand request payload "%s": %s',
                        self.request.body, e)
          raise ApiHandlerException(400)
    return self._payload

  def _UserParentKey(self):
    """Returns a default key to use as parent entity for all User objects.
    
    This is needed for strongly consistent with the High Replication Datastore.
    """
    if self._user_parent_key is None:
      self._user_parent_key = db.Key.from_path('UserRoot', 'vueuser')
    return self._user_parent_key

  def GetUser(self):
    """Returns User object. Creates or queries existing, if necessary.""" 
    if self._user is None:
      if _USER_KEY_ID is not None:
        user_key = db.Key.from_path('User', _USER_KEY_ID,
                                    parent=self._UserParentKey())
        self._user = User.get(user_key)
        if not self._user:
          logging.error('User not found!!')
          raise ApiHandlerException(400)
      else:
        user_cookie = self.request.cookies.get('vueuser')
        if not user_cookie:
          self.CreateUser()
          cookie = base64.encodestring(str(self._user.key().id()))
          logging.info('Set-Cookie: %s', cookie)
          self.response.set_cookie('vueuser', cookie)
        else:
          user_id = int(base64.decodestring(user_cookie))
          user_key = db.Key.from_path('User', user_id, parent=self._UserParentKey())
          self._user = User.get(user_key)
          if not self._user:
            logging.error('User not found!!')
            raise ApiHandlerException(400)
    return self._user

  @staticmethod
  def _UtcNowInMilliSec():
    """Returns current UTC time in milli seconds."""
    return int(time.mktime(datetime.datetime.utcnow().timetuple()) * 1000)
  
  def CreateUser(self):
    """Creates User object and its child AisleList object.
    
    Assigns the created User and AisleList objects to class variables
    self._user and sel._user_aisle_list respectively.
    """
    # TODO: For now, just create temporary user with 'VueUser' as name.
    # Later, this needs to be plugged in with OAuth2
    self._user = User(parent=self._UserParentKey())
    self._user.firstName = 'VueUser'
    self._user.joinTime = self._UtcNowInMilliSec()
    self._user.put()
    key_id = self._user.key().id()
    self._user.lastName = str(key_id)
    self._user.put()
    self._user_aisle_list = AisleList(parent=self._user)
    self._user_aisle_list.put()
       
  def UpdateUser(self):
    """Update the user with the given details in request payload."""
    data_dict = self.GetPayload()
    self.UpdateModel(self.GetUser(), data_dict)

  def DeleteUser(self):
    """Deletes account, all records created by this user and resets Cookie."""
    # TODO: Implement this method
    pass

  def GetUserData(self, user=None, include_aisles=False, include_images=False):
    """Returns UserData as a dict.
    
    Includes aisles details and their images details if required.
    
    Args:
      include_aisles: If true, includes aisles data.
      include_images: If true and also include_aisles is true, includes
                      images data.
    """
    if user is None:
      user = self.GetUser()
      
    user_data = self.ModelToDict(user, include_key_id=False)
    if include_aisles:
      aisle_data = self.GetAllAislesData(include_images)
      user_data['aisles'] = aisle_data
    return user_data
      
  def _GetUserAisleList(self, user):
    """Returns AilesList child entity of a user. Uses self._user if user=None.
    
    Args:
      user: A saved User object.
    Returns:
      AisleList object.
    """
    if user is None:
      user = self.GetUser()
    query = db.GqlQuery('SELECT * from AisleList where ANCESTOR is :1',
                        user.key())
    return query.get()
  
  def GetUserAisleList(self):
    """Returns current user's AisleList object."""
    if self._user_aisle_list is None:
      self._user_aisle_list = self._GetUserAisleList(self.GetUser())
    return self._user_aisle_list
  
  def _AssertImageDataForAisleCreationOrUpdation(self, data):
    """Raises an exception if image data is not compatible to create Aisles.
    
    For creating or updating Aisles, images data should either contain all the
    required fields to create that image or just the "id" field. This is
    required to maintain idempotence of put operation.
    
    Args:
      data: A list of image data dicts, that are passed in aisle creation or
            updation request.

    Raise:
      ApiHandlerException: Raises ApiHandlerException if data is not compatible
                           to create images.
    """
    images_for_creation = []
    for image_dict in data:
      if 'id' in image_dict:
        if len(image_dict) > 1:
          err = ('"id" is present, there should be no other fields. '
                 'Got keys: %s' % image_dict.keys())
          logging.info(err)
          raise ApiHandlerException(err_coode=400, err_msg=err)     
      else:   
        images_for_creation.append(image_dict)
    if images_for_creation:
      self._AssertImageDataForCreation(
          images_for_creation, data_has_aisle_id=False)
  
  def CreateAisles(self, data=None):
    """Creates an Aisle based on supplied data.
    
    Args:
      data: Data supplied as list. Usually the API payload of request
            object converted to list.
    Returns:
      Returns the list of aisles that are created.
    """
    if data is None:
      data = self.GetPayload()
      
    if not isinstance(data, list):
      logging.error('UpdateAisles expects data to be a list, got: %s',
                    type(data))
      raise ApiHandlerException(400)
    
    # We either want to fail all or succeed all entries in the input.
    # So, first run over the data to verify data sanity. 
    for data_dict in data:
      if not isinstance(data_dict, dict):
        logging.error('Expecting dict, got: %s', type(data_dict))
        raise ApiHandlerException(400)
      
      data_dict_keys = data_dict.keys()
      
      if not 'images' in data_dict_keys:
        err = ('"images" data is required for creating aisle. Got keys: %s'
               % data_dict_keys)
        logging.info(err)
        raise ApiHandlerException(err_code=400, err_msg=err)        

      # Assert if Images supplied from Aisle creation are OK
      self._AssertImageDataForAisleCreationOrUpdation(data_dict['images'])

      # Get all the image ids in the request into a list
      image_ids = [img['id'] for img in data_dict['images'] if img.get('id')]      
      # if regImageId field is present, make sure its one of the images
      # that came in the Aisle creation request.
      if ('refImageId' in data_dict_keys and
          data_dict_keys['refImageId'] not in image_ids):
        err = ('"refImageId" (%d) should be one of the image ids that came '
               'along the aisle creation request. Got ids: %s'
               % (data_dict_keys['refImageId'], image_ids))
        logging.info(err)
        raise ApiHandlerException(err_coode=400, err_msg=err)        

      # Now we dont need images for further verification, remove it.
      data_dict_keys.remove('images')  
      if not self.ModelFieldsCompatible(Aisle, data_dict_keys):
        logging.error('Input data not compatible to create Aisle: %s',
                      data_dict)
        raise ApiHandlerException(400)

    # Next loop again and create the aisles.
    user_aisle_list = self.GetUserAisleList()
    aisles = []
    for data_dict in data:
      aisle = Aisle(**data_dict)
      aisle.put()
      aisles.append(aisle)
      image_list = ImageList(parent=aisle)
      # image_list is saved after for loop below

      images_data = data_dict.pop('images')
      # Get all the image ids in the request into a list
      image_ids = [img['id'] for img in images_data if img.get('id')]
      for image_id in image_ids:
        image_list.images.append(db.Key.from_path('Image', image_id))
      image_list.put()

      # Get all the image with out 'id' field
      image_to_create = [
          img for img in images_data if img.get('id') is None]      
      
      images = self.CreateImages(
          image_to_create, aisle_id=aisle.key().id(), verified_data=True)
      
      # Set the reference image id
      if data_dict.get('refImageId'):
        aisle.refImageId = data_dict['refImageId']
      elif images_data[0].get('id'):
        aisle.refImageId = images_data[0]['id']
      else:
        aisle.refImageId = images[0].key().id()
      aisle.put()

      user_aisle_list.aisles.append(aisle.key())
      user_aisle_list.put()

    return aisles

  def UpdateAisles(self, data=None):
    """Updates an existing Aisle with supplied data.
    
    Args:
      data: Data supplied as list. Usually the API payload of request
            object converted to list.
    Returns:
      Returns the list of aisles that are updated.
    """
    if data is None:
      data = self.GetPayload()
      
    if not isinstance(data, list):
      logging.error('UpdateAisles expects data to be a list, got: %s',
                    type(data))
      raise ApiHandlerException(400)

    # We either want to fail all or succeed all entries in the input.
    # So, first run over the data to verify data sanity. 
    for data_dict in data:
      if not isinstance(data_dict, dict):
        logging.error('Expecting dicts, got: %s', data_dict)
        raise ApiHandlerException(400)

      data_dict_keys = data_dict.keys()
      data_dict_keys.remove('id')
      if not self.ModelFieldsCompatible(Aisle, data_dict_keys):
        logging.error('Input data not compatible to create Aisle: %s',
                      data_dict)
        raise ApiHandlerException(400)

    # Next loop again and update the aisles.
    aisles = []
    for data_dict in data:
      # Verified existence of "id" above
      key_id = data_dict.pop('id')
      aisle_key = db.Key.from_path('Aisle', key_id)
      aisle = Aisle.get(aisle_key)
      for key, value in data_dict.iteritems():
        setattr(aisle, key, value)
      aisle.put()
      aisles.append(aisle)
    return aisles

  def DeleteAisles(self, data=None):
    """Deletes an aisle and its ImageList."""
    # TODO: Implement this method.
    # TODO: Understand if images need to be deleted
    pass

  def GetAisleData(self, aisle, include_images=True, include_user=False):
    """Returns aisle data as a dict.
    
    Args:
      aisle: A Aisle objects
      include_images: If True, includes image data. Skips if False.
      include_user: Include user data if True.
      response_format: A json object that defines the schema of the response
                       json.
    Returns:
      A dict containing Aisle data fields.
    """
    aisle_data = self.ModelToDict(aisle)
    if include_images:
      images = self.GetAllImagesOfAisle(aisle)
      images_data = self.GetImagesData(images)
      aisle_data['images'] = images_data
    if include_user:
      aisle_data['user'] = self.ModelToDict(aisle.user)
    return aisle_data

  def GetAllAislesData(self, include_images=True):
    """Returns all the aisles data as a list of aisles."""
    aisles = []
    for aisle_key in self.GetUserAisleList().aisles:
      aisle = Aisle.get(aisle_key)
      aisles.append(aisle)
    return self.GetAislesData(aisles)
  
  
  def _AssertImageDataForCreation(self, data, data_has_aisle_id):
    """Raises an exception if data is not compatible to create images.
    
    Args:
      data: A list of image data dicts, to create images.
      data_has_aisle_id: True if the data contains aisle_id. False otherwise.
    
    Raise:
      ApiHandlerException: Raises ApiHandlerException if data is not compatible
                           to create images.
    """
    if not isinstance(data, list):
      logging.error('CreateImages expects data to be a list, got: %s',
                    data)
      raise ApiHandlerException(400)

    for data_dict in data:
      if not isinstance(data_dict, dict):
        logging.error('Expecting dicts, got: %s', data_dict)
        raise ApiHandlerException(400)

      data_dict_keys = data_dict.keys()
      if data_has_aisle_id:
        if 'aisle_id' not in data_dict_keys:
          logging.error('Expecting "aisle_id" field, got: %s', data_dict)
          raise ApiHandlerException(400)
        data_dict_keys.remove('aisle_id')

      if not self.ModelFieldsCompatible(Image, data_dict_keys):
        logging.error('Input data not compatible to create Images: %s',
                      data_dict)
        raise ApiHandlerException(400)
  
  def CreateImages(self, data=None, aisle_id=None, verified_data=False):
    """Creates an image based on the data provided.
    
    Args:
      data: Data supplied as list. Usually the API payload of request
            object converted to list.
      aisle_id: Aisle key id to be used. Data should not contain 'aisle_id'
                key when aisle_id is provided.
                
    Returns:
      Returns the list of images that are created.
    """
    if data is None:
      data = self.GetPayload()
  
    # We either want to fail all or succeed all entries in the input.
    # So, first run over the data to verify data sanity. 
    if not verified_data:
      data_has_aisle_id = aisle_id is None
      self._AssertImageDataForCreation(data, data_has_aisle_id)
    
    # Next loop again and create the aisles.
    images = []
    for data_dict in data:
      if aisle_id is None:
        # Verified existence of aisle_id above
        aisle_id = data_dict.pop('aisle_id')
      aisle = db.Key.from_path('Aisle', aisle_id)
      image_list = self.GetAisleImageList(aisle)
  
      image = Image(**data_dict)
      image.put()
      images.append(image)
      image_list.images.append(image.key())
      image_list.put()
    return images

  def _AssertImageDataForUpdation(self, data):
    """Raises an exception if data is not compatible to update images.
    
    Args:
      data: A list of image data dicts, to create images.
    
    Raise:
      ApiHandlerException: Raises ApiHandlerException if data is not compatible
                           to update images.
    """
    if not isinstance(data, list):
      logging.error('CreateImages expects data to be a list, got: %s',
                    data)
      raise ApiHandlerException(400)

    for data_dict in data:
      if not isinstance(data_dict, dict):
        logging.error('Expecting dicts, got: %s', data_dict)
        raise ApiHandlerException(400)

      data_dict_keys = data_dict.keys()
      if 'id' not in data_dict_keys:
        logging.error('Expecting "id" field, got: %s', data_dict)
        raise ApiHandlerException(400)
      data_dict_keys.remove('id')
      
      if 'aisle_id' in data_dict_keys:
        data_dict_keys.remove('aisle_id')

      if not self.ModelFieldsCompatible(Image, data_dict_keys):
        logging.error('Input data not compatible to update Images: %s',
                      data_dict)
        raise ApiHandlerException(400)

  def UpdateImages(self, data=None):
    """Updates an image based on the data provided.
    
    Args:
      data: Data supplied as list. Usually the API payload of request
            object converted to list.
    Returns:
      Returns the image that is updated.
    """
    if data is None:
      data = self.GetPayload()
 
    # We either want to fail all or succeed all entries in the input.
    # So, first run over the data to verify data sanity. 
    self._AssertImageDataForUpdation(data)
    
    # Next loop again and create the aisles.
    images = []
    for data_dict in data:      
      # Verified existence of id above
      key_id = data_dict.pop('id')

      image_list = None
      if data_dict.get('aisle_id'):  
        aisle_id = data_dict.pop('aisle_id')    
        aisle = db.Key.from_path('Aisle', aisle_id)
        image_list = self.GetAisleImageList(aisle)

      image_key = db.Key.from_path('Image', key_id)
      image = Image.get(image_key)
      for key, value in data_dict.iteritems():
        setattr(image, key, value)
      image.put()
      images.append(image)

      if image_list is not None:
        image_list.images.append(image.key())
        image_list.put()

    return images

  def GetAisleImageList(self, aisle):
    """Returns ImageList child entity of an aisle.
    
    Args:
      aisle: A saved Aisle object.
    Returns:
      ImageList object.
    """
    query = db.GqlQuery('SELECT * from ImageList WHERE ANCESTOR IS :1',
                        aisle)
    return query.get()
  
  def DeleteImages(self, data=None):
    """Deletes an image.
    
    Args:
      data: Images details, which need to be deleted.
    """
    # TODO: Implement DeleteImage method
    pass

  def GetImagesData(self, images):
    """Returns a list of Image object, of given images list.
    
    Args:
      images: List of Image objects.
    Returns:
      A list of Image object data fields as dict.
    """
    images_data = []
    for image in images:
      images_data.append(self.ModelToDict(image))
    return images_data
    
  def GetAllImagesOfAisle(self, aisle):
    """Returns a list of image data (as dict) from a given aisle.
    
    Args:
      aisle: Aisle object whose images need to be gathered.
    Returns:
      A list of image data dicts under the given Aisle.
    """
    image_list = []
    aisle_image_list = self.GetAisleImageList(aisle)
    for image_key in aisle_image_list.images:
      image = Image.get(image_key)
      image_list.append(image)
    return image_list

  def ModelToDict(self, model, include_key_id=True,
                  parent_key_id_field=None):
    model_dict = {}
    for field, value in db.to_dict(model).iteritems():
      if value:
        # TODO: Add type checking, compatible with Json datatypes.
        model_dict[field] = value    

    if include_key_id and model.is_saved:
      key_id = model.key().id()
      if key_id:
        model_dict['id'] = key_id


    if parent_key_id_field:
      parent = model.parent()
      if parent is not None:
        model_dict[parent_key_id_field] = parent.key().id()
    
    return model_dict

  def ModelToJson(self, model, include_key_id=True,
                  parent_key_id_field=None):
    json_dict = self.ModelToDict(model, include_key_id, parent_key_id_field)
    return json.dumps(json_dict)

  def UpdateModel(self, model, data_dict):
    if not isinstance(model, db.Model):
      logging.error('Entity %s is not of type db.modal', model)
      raise ApiHandlerException(500)
    
    input_fields = set(data_dict.keys())
    model_fields = set(model.fields().keys())
    if not model_fields.issuperset(input_fields):
      logging.error('Unknown fields provided: %s', list(input_fields))
      raise ApiHandlerException(400)

    for key, value in data_dict.iteritems():
      setattr(model, key, value)
    model.put()

  # TODO: check for required fields constraint
  def ModelFieldsCompatible(self, model_class, input_fields):
    """Raises exception if input_fields are not compatible with model fields.
    
    Args:
      model: Datastore Entity model name as string.
      input_fields: A list of input fields that we are asserting against.
    Returns:
      True if the model and input_fields are compatible. False otherwise.
    """
    model_fields = set(model_class.fields())
    if model_fields.issuperset(set(input_fields)):
      return True
    else:
      return False

  def GetAislesData(self, aisles, response_format=None):
    """Returns the trending aisles from all users.
    
    Args:
      aisles: List of aisles
      response_format: A json object that represents the response json schema
    Returns:
      list of Aisle data.
    """
    aisles_data = []
    #for aisle in Aisle.all().order('name').run(limit=limit, offset=offset):
    for aisle in aisles:
      if not aisle:
        continue
      aisle_data = self.GetAisleData(aisle, include_images=True,
                                     include_user=True)
      #TODO: Quick and dirty hack.
      if response_format:
        tmp_aisle_data = {}
        for key in response_format:
          tmp_aisle_data[key] = aisle_data.get(key)
        aisle_data = tmp_aisle_data
          
      aisles_data.append(aisle_data)
    return aisles_data

  # TODO: Implement paging using cursors. 
  def GetTrendingAislesData(self, limit=5, offset=0, response_format=None):
    """Returns the trending aisles from all users.
    
    Args:
      limit: Limit number of aisles returned to this number.
      offset: Start from this number.
    Returns:
      list of Aisle data.
    """
    aisles_data = []
    #for aisle in Aisle.all().order('name').run(limit=limit, offset=offset):
    for aisle in Aisle.all().run(limit=limit, offset=offset):
      aisle_data = self.GetAisleData(aisle, include_images=True,
                                     include_user=True)
      #TODO: Quick and dirty hack.
      if response_format:
        tmp_aisle_data = {}
        for key in response_format:
          tmp_aisle_data[key] = aisle_data.get(key)
        aisle_data = tmp_aisle_data
          
      aisles_data.append(aisle_data)
    return aisles_data

  def ProcessGetAisle(self):
    if not self._model_args:
      if self.request.GET.get('ids'):
        aisle_ids = [int(i) for i in self.request.GET.get('ids').split(',')]
        aisles = Aisle.get_by_id(aisle_ids)
        request_format = None
        if self.request.GET.get('rf'):
          request_format = json.loads(self.request.GET.get('rf'))
        aisles_data = self.GetAislesData(aisles, request_format)
        self.response.out.write(json.dumps(aisles_data))
    elif self._model_args and self._model_args[0] == 'trending':
      args = {}
      if self.request.GET.get('limit'):
        args['limit'] = int(self.request.GET.get('limit'))
      if self.request.GET.get('offset'):
        args['offset'] = int(self.request.GET.get('offset'))
      # Response format
      if self.request.GET.get('rf'):
        args['response_format'] = json.loads(self.request.GET.get('rf'))
      aisles_data = self.GetTrendingAislesData(**args)
      self.response.out.write(json.dumps(aisles_data))
    else:
      self.response.out.write(json.dumps(self.GetAllAislesData()))
    
  #
  # Overloaded methods from webapp2.RequestHandler.
  #
  def get(self):
    self.response.headers['Content-Type'] = 'application/json'
    if self._model == 'user':
      user_data = self.GetUserData(include_aisles=False, include_images=False)
      self.response.out.write(json.dumps(user_data))
      ##
    elif self._model == 'aisle':
      self.ProcessGetAisle()
    elif self._model == 'image':
      pass
    else:
      raise ApiHandlerException(400)
    
  # POST is for updates
  def post(self):
    if self._model == 'user':
      self.UpdateUser()
      user_data = self.GetUserData(include_aisles=True, include_images=True)
      self.response.out.write(json.dumps(user_data))
    elif self._model == 'aisle':
      aisles = self.UpdateAisles()
      self.response.out.write(json.dumps(self.GetAislesData(aisles)))
    elif self._model == 'image':
      images = self.UpdateImages()
      self.response.out.write(json.dumps(self.GetImagesData(images)))
    else:
      raise ApiHandlerException(400)
    
  # PUT is for creates
  def put(self):
    if self._model == 'user':
      logging.error('Cannot use PUT method for "user" updates.')
      raise ApiHandlerException(400)
    elif self._model == 'aisle':
      aisles = self.CreateAisles()
      self.response.out.write(json.dumps(self.GetAislesData(aisles)))
    elif self._model == 'image':
      images = self.CreateImages()
      self.response.out.write(json.dumps(self.GetImagesData(images)))
    else:
      raise ApiHandlerException(400) 
  
  def delete(self):
    if self._model == 'user':
      self.DeleteUser()
    elif self._model == 'aisle':
      self.DeleteAisles()
    elif self._model == 'image':
      self.DeleteImages()
    else:
      raise ApiHandlerException(400)
  
  # TODO: Implement better error responses
  def handle_exception(self, exception, debug_mode):
    if(isinstance(exception, ApiHandlerException)):
      # if None, assume thrower has configured the response appropriately
      if(exception.err_code is not None):
        if(exception.err_code < 400):
          self.response.clear()
          self.response.set_status(exception.err_code)
        else:
          self.error(exception.err_code)
          self.response.headers['Content-Type'] = 'application/json'
          # TODO: Investigate how to write detailed error messages only when
          # the backend is running in debug mode.
          self.response.out.write(json.dumps(exception.ToDict()))
    else:
      super(ApiHandler, self).handle_exception(exception, debug_mode)


def prefetch_references(entities, *props):
    fields = [(entity, prop) for entity in entities for prop in props]
    ref_keys = [prop.get_value_for_datastore(x) for x, prop in fields]
    ref_entities = dict((x.key(), x) for x in db.get(set(ref_keys)))
    for (entity, prop), ref_key in zip(fields, ref_keys):
        prop.__set__(entity, ref_entities[ref_key])
    return entities
  

class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    self.response.out.write(
        '<html><body><img style="display:block;margin-left:auto;'
        'margin-right:auto" src="http://imgs.xkcd.com/comics/'
        'exploits_of_a_mom.png"/></body></html>')

    
# TODO: This piece of code is for displaying application stats.
# Should be disabled before production deployment.
def webapp_add_wsgi_middleware(app):
    from google.appengine.ext.appstats import recording
    app = recording.appstats_wsgi_middleware(app)
    return app

# TODO: debug is set to True for ease of testing. Remove before production
# deployment.
app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/rest.*', ApiHandler),
], debug=True)

app = webapp_add_wsgi_middleware(app)


def main():
  app.RUN()


if __name__ == '__main__':
  main()

