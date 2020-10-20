from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from auth_token.models import AuthToken
from data_source.models import DataSource
from utils.common.constants import STATUS_PUBLISHED
from django.conf import settings
from django.contrib.auth import get_user_model


class TokenAuthentication(BaseAuthentication):
    """ 验证项目绑定账号的 Token 是否有效 """
    keyword = 'token'

    # @staticmethod
    # def get_data_source(request):
    #     data = request.POST
    #     try:
    #         data_source = data['data_source']
    #     except KeyError:
    #         data_source = None
    #     return data_source

    def get_token(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            raise AuthenticationFailed('no Authenticate Token found in headers')

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Token string should not contain spaces.'
            raise AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise AuthenticationFailed(msg)
        return token

    def authenticate(self, request):
        # data_source = self.get_data_source(request)
        token = self.get_token(request)

        try:
            token = AuthToken.objects.select_related('owner').get(token=token)
        except AuthToken.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.owner.is_active:
            raise AuthenticationFailed('User inactive or deleted.')

        try:
            # ds = DataSource.objects.get(label=data_source)
            if token.status is STATUS_PUBLISHED and not token.is_expired:
                return token.user, token
            else:
                raise AuthenticationFailed('token not belong to this project')
        except (DataSource.DoesNotExist, DataSource.MultipleObjectsReturned):
            raise AuthenticationFailed('no project registered or project registered more then one')


class RestAPIAuthentication(TokenAuthentication):
    """WebHook 通过 url 传递 token"""

    def get_token(self, request):
        try:
            token = request.query_params.get(self.keyword)
        except Exception as e:
            raise AuthenticationFailed(str(e))

        return token

    def authenticate(self, request):
        if settings.DEBUG:
            user_model = get_user_model()
            admin = user_model.objects.get(username='admin')
            return admin, ""
        else:
            return super(RestAPIAuthentication, self).authenticate(request)


# class PrometheusAuthentication(RestFulAuthentication):
#     """ project = prometheus """
# 
#     @staticmethod
#     def get_project(request):
#         return "prometheus"