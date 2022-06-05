# API messages

USER_DOES_NOT_EXIST_ERROR = "user does not exist"
ARTICLE_DOES_NOT_EXIST_ERROR = "article does not exist"
ARTICLE_ALREADY_EXISTS = "article already exists"
USER_IS_NOT_AUTHOR_OF_ARTICLE = "you are not an author of this article"
USER_IS_NOT_AUTHOR_OF_EVENT = "you are not an author of this event"

POST_DOES_NOT_EXISTS = "Post does not exists"

EVENT_DOES_NOT_EXIST_ERROR = "Event does not exist"
EVENT_ALREADY_EXISTS = "Event already exists"

PROFILE_DOES_NOT_EXISTS = "Profile does not exists"

VEHICLE_ALREADY_EXISTS = "Vehicle already exists"
VEHICLE_CONFLICT_VIN_ERROR = "Vehicle with current VIN already exist"
VEHICLE_CONFLICT_REGISTRATION_PLATE_ERROR = "Vehicle with current REGISTRATION PLATE already exist"
VEHICLE_DOES_NOT_EXIST_ERROR = "Vehicle does not exist"
VEHICLE_CONFLICT_VIN_OR_REG_PLATE = "Vehicle with current VIN or REGISTRATION PLATE already exists"
VEHICLE_CREATE_ERROR = "Vehicle create error"
VEHICLE_GET_ERROR = "Vehicle get error"
VEHICLE_UPDATE_ERROR = "Vehicle update error"
VEHICLE_DELETE_ERROR = "Vehicle delete error"
VEHICLE_MILEAGE_REDUCE = "Vehicle mileage can't reduced"

SERVICE_CREATE_ERROR = "Service create error"
SERVICE_GET_ERROR = "Service get error"
SERVICE_UPDATE_ERROR = "Service update error"
SERVICE_DELETE_ERROR = "Service delete error"
SERVICE_TYPE_DOES_NOT_EXIST_ERROR = "Service type doesn't exist"
SERVICE_DOES_NOT_EXIST_ERROR = "Service does not exist"

REMINDER_CREATE_ERROR = "Reminder create error"
REMINDER_GET_ERROR = "Reminder get error"
REMINDER_UPDATE_ERROR = "Reminder update error"
REMINDER_DELETE_ERROR = "Reminder delete error"
REMINDER_TYPE_DOES_NOT_EXIST_ERROR = "Reminder type doesn't exist"
REMINDER_DOES_NOT_EXIST_ERROR = "Reminder does not exist"

FUEL_CREATE_ERROR = "Fuel create error"
FUEL_GET_ERROR = "Reminder get error"
FUEL_UPDATE_ERROR = "Reminder update error"
FUEL_DELETE_ERROR = "Reminder delete error"
FUEL_TYPE_DOES_NOT_EXIST_ERROR = "Reminder type doesn't exist"
FUEL_DOES_NOT_EXIST_ERROR = "Reminder does not exist"

LOCATION_DOES_NOT_EXIST_ERROR = "Location doesn't exist"

INCORRECT_LOGIN_INPUT = "incorrect username or password"
USERNAME_TAKEN = "user with this username already exists"
EMAIL_TAKEN = "user with this email already exists"

UNABLE_TO_FOLLOW_YOURSELF = "user can not follow him self"
UNABLE_TO_UNSUBSCRIBE_FROM_YOURSELF = "user can not unsubscribe from him self"
USER_IS_NOT_FOLLOWED = "you don't follow this user"
USER_IS_ALREADY_FOLLOWED = "you follow this user already"

WRONG_TOKEN_PREFIX = "unsupported authorization type"  # noqa: S105
MALFORMED_PAYLOAD = "could not validate credentials"

ARTICLE_IS_ALREADY_FAVORITED = "you are already marked this articles as favorite"
ARTICLE_IS_NOT_FAVORITED = "article is not favorited"

COMMENT_DOES_NOT_EXIST = "comment does not exist"

AUTHENTICATION_REQUIRED = "authentication required"
