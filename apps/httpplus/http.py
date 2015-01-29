# -*- coding: utf-8 -*-

from django.http import *

class HttpResponseCreated(HttpResponse):
    status_code = 201

class HttpResponseAccepted(HttpResponse):
    status_code = 201

class HttpResponseNonAuthoritativeInformation(HttpResponse):
    status_code = 203

class HttpResponseNoContent(HttpResponse):
    status_code = 204

    def __init__(self, content='', mimetype=None, status=None,
            content_type=None):
        return super(HttpResponseNoContent, self).__init__(
            content='',
            mimetype=mimetype,
            status=None,
            content_type=content_type
        )

class HttpResponseResetContent(HttpResponse):
    status_code = 205

class HttpResponsePartialContent(HttpResponse):
    status_code = 206

class HttpResponseMultipleChoices(HttpResponse):
    status_code = 300

class HttpResponseMovedPermanently(HttpResponsePermanentRedirect):
    pass

class HttpResponseFound(HttpResponseRedirect):
    pass

class HttpResponseSeeOther(HttpResponse):
    status_code = 303

class HttpResponseUseProxy(HttpResponse):
    status_code = 305

class HttpResponseTemporaryRedirect(HttpResponseRedirect):
    status_code = 307

class HttpResponseResumeIncomplete(HttpResponse):
    status_code = 308

class HttpResponseUnauthorized(HttpResponse):
    status_code = 401

class HttpResponsePaymentRequired(HttpResponse):
    status_code = 402

class HttpResponseMethodNotAllowed(HttpResponseNotAllowed):
    pass

class HttpResponseNotAcceptable(HttpResponse):
    status_code = 406

class HttpResponseProxyAuthenticationRequired(HttpResponse):
    status_code = 407

class HttpResponseRequestTimeout(HttpResponse):
    status_code = 408

class HttpResponseConflict(HttpResponse):
    status_code = 409

class HttpResponseGone(HttpResponse):
    status_code = 410

class HttpResponseLengthRequired(HttpResponse):
    status_code = 411

class HttpResponsePreconditionFailed(HttpResponse):
    status_code = 412

class HttpResponseRequestEntityTooLarge(HttpResponse):
    status_code = 413

class HttpResponseRequestUriTooLong(HttpResponse):
    status_code = 414

class HttpResponseUnsupportedMediaType(HttpResponse):
    status_code = 415

class HttpResponseRequestRangeNotSatisfiable(HttpResponse):
    status_code = 416

class HttpResponseExpectationFailed(HttpResponse):
    status_code = 417

class HttpResponseFieldValidationError(HttpResponse):
    status_code = 422

class HttpResponseInternalServerError(HttpResponse):
    status_code = 500

class HttpResponseNotImplemented(HttpResponse):
    status_code = 501

class HttpResponseBadGateway(HttpResponse):
    status_code = 502

class HttpResponseServiceUnavailable(HttpResponse):
    status_code = 503

class HttpResponseGatewayTimeout(HttpResponse):
    status_code = 504

class HttpResponseHttpVersionNotSupported(HttpResponse):
    status_code = 505

HTTP_RESPONSE_CLASS_TUPLE = (
    (200, HttpResponse),
    (201, HttpResponseCreated),
    (202, HttpResponseAccepted),
    (203, HttpResponseNonAuthoritativeInformation),
    (204, HttpResponseNoContent),
    (205, HttpResponseResetContent),
    (206, HttpResponsePartialContent),
    (300, HttpResponseMultipleChoices),
    (301, HttpResponseMovedPermanently),
    (302, HttpResponseFound),
    (303, HttpResponseSeeOther),
    (304, HttpResponseNotModified),
    (305, HttpResponseUseProxy),
    (307, HttpResponseTemporaryRedirect),
    (400, HttpResponseBadRequest),
    (401, HttpResponseUnauthorized),
    (402, HttpResponsePaymentRequired),
    (403, HttpResponseForbidden),
    (404, HttpResponseNotFound),
    (405, HttpResponseMethodNotAllowed),
    (406, HttpResponseNotAcceptable),
    (407, HttpResponseProxyAuthenticationRequired),
    (408, HttpResponseRequestTimeout),
    (409, HttpResponseConflict),
    (410, HttpResponseGone),
    (411, HttpResponseLengthRequired),
    (412, HttpResponsePreconditionFailed),
    (413, HttpResponseRequestEntityTooLarge),
    (414, HttpResponseRequestUriTooLong),
    (415, HttpResponseUnsupportedMediaType),
    (416, HttpResponseRequestRangeNotSatisfiable),
    (417, HttpResponseExpectationFailed),
    (500, HttpResponseInternalServerError),
    (501, HttpResponseNotImplemented),
    (502, HttpResponseBadGateway),
    (503, HttpResponseServiceUnavailable),
    (504, HttpResponseGatewayTimeout),
    (505, HttpResponseHttpVersionNotSupported),
)

HTTP_RESPONSE_CLASS_MAP = dict(HTTP_RESPONSE_CLASS_TUPLE)
