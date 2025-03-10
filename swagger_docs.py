from flambda_app.logging import get_logger
from flambda_app.openapi import api_schemas
from flambda_app.openapi import spec, generate_openapi_yml
from app import (turnstile_list, turnstile_get, turnstile_create, turnstile_update,
                 turnstile_delete, access_create, access_records)

LOGGER = get_logger(force=True)

# *************
# turnstile
# *************
spec.path(
    view=turnstile_list,
    path="/v1/turnstile",
    operations={
        'get': {
            'summary': 'Get Turnstile List',
            'description': 'This endpoint retrieves a list of turnstiles with their details.',
            'parameters': [
                {
                    'name': 'limit',
                    'in': 'query',
                    'description': 'Number of items to return',
                    'required': False,
                    'schema': {
                        'type': 'integer',
                        'example': 20
                    }
                },
                {
                    'name': 'offset',
                    'in': 'query',
                    'description': 'Offset for pagination',
                    'required': False,
                    'schema': {
                        'type': 'integer',
                        'example': 0
                    }
                },
                {
                    'name': 'fields',
                    'in': 'query',
                    'description': 'Comma-separated list of fields to return',
                    'required': False,
                    'schema': {
                        'type': 'string',
                        'example': 'id,name,is_active'
                    }
                },
                {
                    'name': 'order_by',
                    'in': 'query',
                    'description': 'Order the list by a given field',
                    'required': False,
                    'schema': {
                        'type': 'string',
                        'example': 'name'
                    }
                }
            ],
            'responses': {
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'success': {
                                        'type': 'boolean',
                                        'example': True
                                    },
                                    'label': {
                                        'type': 'string',
                                        'example': 'common.success'
                                    },
                                    'code': {
                                        'type': 'integer',
                                        'example': 1
                                    },
                                    'message': {
                                        'type': 'string',
                                        'example': 'Success'
                                    },
                                    'params': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'string'
                                        },
                                        'example': []
                                    },
                                    'data': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'id': {
                                                    'type': 'integer',
                                                    'example': 1
                                                },
                                                'uuid': {
                                                    'type': 'string',
                                                    'example': '7d61832e-f93f-11ef-90a2'
                                                               '-0242ac130005'
                                                },
                                                'name': {
                                                    'type': 'string',
                                                    'example': 'João da Silva'
                                                },
                                                'is_active': {
                                                    'type': 'integer',
                                                    'example': 0
                                                },
                                                'created_at': {
                                                    'type': 'string',
                                                    'example': '2025-03-10 17:10:31'
                                                },
                                                'updated_at': {
                                                    'type': 'string',
                                                    'example': '2025-03-10 17:10:31'
                                                },
                                                'deleted_at': {
                                                    'type': 'string',
                                                    'nullable': True,
                                                    'example': None
                                                }
                                            }
                                        }
                                    },
                                    'control': {
                                        'type': 'object',
                                        'properties': {
                                            'offset': {
                                                'type': 'integer',
                                                'example': 0
                                            },
                                            'limit': {
                                                'type': 'integer',
                                                'example': 20
                                            },
                                            'total': {
                                                'type': 'integer',
                                                'example': 2
                                            },
                                            'count': {
                                                'type': 'integer',
                                                'example': 2
                                            }
                                        }
                                    },
                                    'meta': {
                                        'type': 'object',
                                        'properties': {
                                            'href': {
                                                'type': 'string',
                                                'example': 'http://localhost:5000/v1/turnstile?'
                                            },
                                            'next': {
                                                'type': 'string',
                                                'example': ''
                                            },
                                            'previous': {
                                                'type': 'string',
                                                'example': ''
                                            },
                                            'first': {
                                                'type': 'string',
                                                'example': ''
                                            },
                                            'last': {
                                                'type': 'string',
                                                'example': ''
                                            }
                                        }
                                    },
                                    'links': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
)

spec.path(
    view=turnstile_get,
    path="/v1/turnstile/{uuid}",
    operations={
        'get': {
            'summary': 'Get Turnstile by UUID',
            'description': 'Retrieve details of a specific turnstile using its UUID.',
            'parameters': [
                {
                    'name': 'uuid',
                    'in': 'path',
                    'description': 'UUID of the turnstile to retrieve',
                    'required': True,
                    'schema': {
                        'type': 'string',
                        'example': '6d61832e-f93f-11ef-90a2-0242ac130005'
                    }
                }
            ],
            'responses': {
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'success': {'type': 'boolean', 'example': True},
                                    'label': {'type': 'string', 'example': 'common.success'},
                                    'code': {'type': 'integer', 'example': 1},
                                    'message': {'type': 'string', 'example': 'Success'},
                                    'params': {'type': 'array', 'items': {'type': 'string'}, 'example': []},
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {'type': 'integer', 'example': 2},
                                            'uuid': {'type': 'string', 'example': '6d61832e-f93f-11ef-90a2-0242ac130005'},
                                            'name': {'type': 'string', 'example': 'Maria Eduarda'},
                                            'is_active': {'type': 'integer', 'example': 1},
                                            'created_at': {'type': 'string', 'example': '2025-03-10 17:12:49'},
                                            'updated_at': {'type': 'string', 'example': '2025-03-10 17:12:49'},
                                            'deleted_at': {'type': 'string', 'nullable': True, 'example': None}
                                        }
                                    },
                                    'control': {
                                        'type': 'object',
                                        'properties': {
                                            'offset': {'type': 'integer', 'example': 0},
                                            'limit': {'type': 'integer', 'example': 20},
                                            'total': {'type': 'integer', 'example': 1},
                                            'count': {'type': 'integer', 'example': 1}
                                        }
                                    },
                                    'meta': {
                                        'type': 'object',
                                        'properties': {
                                            'href': {'type': 'string', 'example': 'http://localhost:5000/v1/turnstile/6d61832e-f93f-11ef-90a2-0242ac130005?'},
                                            'next': {'type': 'string', 'example': ''},
                                            'previous': {'type': 'string', 'example': ''},
                                            'first': {'type': 'string', 'example': ''},
                                            'last': {'type': 'string', 'example': ''}
                                        }
                                    },
                                    'links': {
                                        'type': 'array',
                                        'items': {
                                            'type': 'object',
                                            'properties': {
                                                'href': {'type': 'string', 'example': 'http://localhost:5000/v1/turnstile/6d61832e-f93f-11ef-90a2-0242ac130005'},
                                                'rel': {'type': 'string', 'example': 'update'},
                                                'method': {'type': 'string', 'example': 'UPDATE'}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '400': {
                    'description': 'Bad Request',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'success': {'type': 'boolean', 'example': False},
                                    'code': {'type': 'integer', 'example': 31},
                                    'label': {'type': 'string', 'example': 'common.error.validation_error'},
                                    'message': {'type': 'string', 'example': 'Validation error, please review your params: value (7d61832e-f93f-11ef-90a2-0242ac130005) for param (uuid)'},
                                    'params': {'type': 'array', 'items': {'type': 'string'}, 'example': ['7d61832e-f93f-11ef-90a2-0242ac130005', 'uuid']}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
)

spec.path(
    view=turnstile_create,
    path="/v1/turnstile",
    operations={
        'post': {
            'summary': 'Create a new Turnstile',
            'description': 'Create a new turnstile with the given details.',
            'requestBody': {
                'required': True,
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string', 'example': 'Maria Eduarda'},
                                'is_active': {'type': 'boolean', 'example': True},
                                'uuid': {'type': 'string', 'example': '6d61832e-f93f-11ef-90a2-0242ac130005'}
                            }
                        }
                    }
                }
            },
            'responses': {
                '200': {
                    'description': 'Successful response',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'success': {'type': 'boolean', 'example': True},
                                    'label': {'type': 'string', 'example': 'common.success'},
                                    'code': {'type': 'integer', 'example': 1},
                                    'message': {'type': 'string', 'example': 'Success'},
                                    'params': {'type': 'array', 'items': {'type': 'string'}, 'example': []},
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {'type': 'integer', 'example': 2},
                                            'uuid': {'type': 'string', 'example': '6d61832e-f93f-11ef-90a2-0242ac130005'},
                                            'name': {'type': 'string', 'example': 'Maria Eduarda'},
                                            'is_active': {'type': 'boolean', 'example': True},
                                            'created_at': {'type': 'string', 'example': '2025-03-10T17:12:49.292286'},
                                            'updated_at': {'type': 'string', 'nullable': True, 'example': None},
                                            'deleted_at': {'type': 'string', 'nullable': True, 'example': None}
                                        }
                                    },
                                    'control': {
                                        'type': 'object',
                                        'properties': {
                                            'offset': {'type': 'integer', 'example': 0},
                                            'limit': {'type': 'integer', 'example': 20},
                                            'total': {'type': 'integer', 'example': 1},
                                            'count': {'type': 'integer', 'example': 1}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
)

spec.path(
    view=turnstile_update,
    path="/v1/turnstile/{uuid}",
    operations={
        'patch': {
            'summary': 'Update Turnstile by UUID',
            'description': 'Update the details of an existing turnstile by its UUID.',
            'parameters': [
                {
                    'name': 'uuid',
                    'in': 'path',
                    'description': 'UUID of the turnstile to update',
                    'required': True,
                    'schema': {
                        'type': 'string',
                        'example': '6d61832e-f93f-11ef-90a2-0242ac130005'
                    }
                }
            ],
            'requestBody': {
                'required': True,
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'name': {'type': 'string', 'example': 'João da Silva'},
                                'is_active': {'type': 'boolean', 'example': False},
                                'uuid': {'type': 'string', 'example': '7d61832e-f93f-11ef-90a2-0242ac130005'}
                            }
                        }
                    }
                }
            },
            'responses': {
                '200': {
                    'description': 'Successful update response',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'success': {'type': 'boolean', 'example': True},
                                    'label': {'type': 'string', 'example': 'common.success'},
                                    'code': {'type': 'integer', 'example': 1},
                                    'message': {'type': 'string', 'example': 'Success'},
                                    'params': {'type': 'array', 'items': {'type': 'string'}, 'example': []},
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {'type': 'integer', 'example': 2},
                                            'uuid': {'type': 'string', 'example': '6d61832e-f93f-11ef-90a2-0242ac130005'},
                                            'name': {'type': 'string', 'example': 'João da Silva'},
                                            'is_active': {'type': 'boolean', 'example': False},
                                            'created_at': {'type': 'string', 'example': '2025-03-10 17:12:49'},
                                            'updated_at': {'type': 'string', 'example': '2025-03-10 14:30:47.131495-03:00'},
                                            'deleted_at': {'type': 'string', 'nullable': True, 'example': None}
                                        }
                                    },
                                    'control': {
                                        'type': 'object',
                                        'properties': {
                                            'offset': {'type': 'integer', 'example': 0},
                                            'limit': {'type': 'integer', 'example': 20},
                                            'total': {'type': 'integer', 'example': 1},
                                            'count': {'type': 'integer', 'example': 1}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '400': {
                    'description': 'Bad request due to validation error',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'success': {'type': 'boolean', 'example': False},
                                    'code': {'type': 'integer', 'example': 31},
                                    'label': {'type': 'string', 'example': 'common.error.validation_error'},
                                    'message': {'type': 'string', 'example': 'Validation error, please review your params: value (7d61832e-f93f-11ef-90a2-0242ac130005) for param (uuid)'},
                                    'params': {'type': 'array', 'items': {'type': 'string'}, 'example': ['7d61832e-f93f-11ef-90a2-0242ac130005', 'uuid']}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
)

spec.path(
    view=turnstile_delete,
    path="/v1/turnstile/{uuid}",
    operations={
        'delete': {
            'summary': 'Delete Turnstile by UUID',
            'description': 'Delete a specific turnstile identified by UUID.',
            'parameters': [
                {
                    'name': 'uuid',
                    'in': 'path',
                    'description': 'UUID of the turnstile to delete',
                    'required': True,
                    'schema': {
                        'type': 'string',
                        'example': '6d61832e-f93f-11ef-90a2-0242ac130005'
                    }
                }
            ],
            'responses': {
                '200': {
                    'description': 'Successful deletion response',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'success': {'type': 'boolean', 'example': True},
                                    'label': {'type': 'string', 'example': 'common.success'},
                                    'code': {'type': 'integer', 'example': 1},
                                    'message': {'type': 'string', 'example': 'Success'},
                                    'params': {'type': 'array', 'items': {'type': 'string'}, 'example': []},
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'deleted': {'type': 'boolean', 'example': True}
                                        }
                                    },
                                    'control': {
                                        'type': 'object',
                                        'properties': {
                                            'offset': {'type': 'integer', 'example': 0},
                                            'limit': {'type': 'integer', 'example': 20},
                                            'total': {'type': 'integer', 'example': 1},
                                            'count': {'type': 'integer', 'example': 1}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                '400': {
                    'description': 'Bad request due to error while updating record',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'success': {'type': 'boolean', 'example': False},
                                    'code': {'type': 'integer', 'example': 18},
                                    'label': {'type': 'string', 'example': 'common.error'
                                                                           '.update_error'},
                                    'message': {'type': 'string', 'example': 'Unable to update '
                                                                             'the record'},
                                    'params': {'type': 'null'},
                                    'details': {'type': 'null'},
                                    'trace': {'type': 'string', 'example': 'Traceback (most '
                                                                           'recent call last): ...'}
                                }
                            }
                        }
                    }
                }
            }
        }
    }
)

# *************
# access
# *************

spec.path(
    view=access_create,
    path="/v1/access",
    operations={
        'post': {
            'summary': 'Register an access event',
            'description': 'Logs an access event (entry, exit, or blocked) for a turnstile.',
            'requestBody': {
                'required': True,
                'content': {
                    'application/json': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'type': {
                                    'type': 'string',
                                    'enum': ['entry', 'exit', 'blocked'],
                                    'example': 'entry'
                                },
                                'timestamp': {'type': 'string', 'example': '2025-03-04 15:30:00'},
                                'turnstile_uuid': {'type': 'string', 'example': '7d61832e-f93f-11ef-90a2-0242ac130005'}
                            }
                        }
                    }
                }
            },
            'responses': {
                '200': {
                    'description': 'Successful registration of access event',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'success': {'type': 'boolean', 'example': True},
                                    'label': {'type': 'string', 'example': 'common.success'},
                                    'code': {'type': 'integer', 'example': 1},
                                    'message': {'type': 'string', 'example': 'Success'},
                                    'params': {'type': 'array', 'items': {'type': 'string'}, 'example': []},
                                    'data': {
                                        'type': 'object',
                                        'properties': {
                                            'id': {'type': 'integer', 'example': 2},
                                            'type': {'type': 'string', 'example': 'entry'},
                                            'timestamp': {'type': 'string', 'example': '2025-03-04 15:30:00'},
                                            'created_at': {'type': 'string', 'example': '2025-03-10T17:59:53.549672'},
                                            'updated_at': {'type': 'string', 'nullable': True, 'example': None},
                                            'deleted_at': {'type': 'string', 'nullable': True, 'example': None},
                                            'turnstile_uuid': {'type': 'string', 'example': '6d61832e-f93f-11ef-90a2-0242ac130007'}
                                        }
                                    },
                                    'control': {
                                        'type': 'object',
                                        'properties': {
                                            'offset': {'type': 'integer', 'example': 0},
                                            'limit': {'type': 'integer', 'example': 20},
                                            'total': {'type': 'integer', 'example': 1},
                                            'count': {'type': 'integer', 'example': 1}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
)

spec.path(
    view=access_records,
    path="/v1/access/{turnstile_uuid}",
    operations={
        'get': {
            'summary': 'Retrieve access records for a turnstile',
            'description': 'Fetches all access records related to a given turnstile by UUID.',
            'parameters': [
                {
                    'name': 'turnstile_uuid',
                    'in': 'path',
                    'description': 'UUID of the turnstile',
                    'required': True,
                    'schema': {
                        'type': 'string',
                        'example': '6d61832e-f93f-11ef-90a2-0242ac130007'
                    }
                }
            ],
            'responses': {
                '200': {
                    'description': 'Successful retrieval of access records',
                    'content': {
                        'application/json': {
                            'schema': {
                                'type': 'object',
                                'properties': {
                                    'success': {'type': 'boolean', 'example': True},
                                    'label': {'type': 'string', 'example': 'common.success'},
                                    'code': {'type': 'integer', 'example': 1},
                                    'message': {'type': 'string', 'example': 'Success'},
                                    'params': {'type': 'array', 'items': {'type': 'string'}, 'example': []},
                                    'data': {
                                        'type': 'object',
                                        'nullable': True,
                                        'properties': {
                                            'uuid': {'type': 'string', 'example': '6d61832e-f93f-11ef-90a2-0242ac130007'},
                                            'name': {'type': 'string', 'example': 'Maria Eduarda'},
                                            'is_active': {'type': 'integer', 'example': 1},
                                            'created_at': {'type': 'string', 'example': '2025-03-10 17:58:47'},
                                            'updated_at': {'type': 'string', 'example': '2025-03-10 17:58:46'},
                                            'deleted_at': {'type': 'string', 'nullable': True, 'example': None},
                                            'access_records': {
                                                'type': 'array',
                                                'items': {
                                                    'type': 'object',
                                                    'properties': {
                                                        'type': {'type': 'string', 'example': 'entry'},
                                                        'timestamp': {'type': 'string', 'example': '2025-03-04 15:30:00'}
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    'control': {
                                        'type': 'object',
                                        'properties': {
                                            'offset': {'type': 'integer', 'example': 0},
                                            'limit': {'type': 'integer', 'example': 20},
                                            'total': {'type': 'integer', 'example': 1},
                                            'count': {'type': 'integer', 'example': 1}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
)


if __name__ == "__main__":
    generate_openapi_yml(spec, LOGGER, force=True)
    api_schemas.register()
