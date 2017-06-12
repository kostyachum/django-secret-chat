import json

import hashlib

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, FormView, ListView
from django.views.generic.detail import SingleObjectMixin, DetailView

from chaton.forms import MessageForm, ChatForm, ChatLoginForm, MessageRespondForm
from chaton.models import UserChatList
from . import models, config


class ChatCreateView(CreateView):
    model = models.Chat
    form_class = ChatForm
    template_name = 'new.html'

    def get_success_url(self):
        return reverse('chat', kwargs={'hash': self.object.hash})

    def form_valid(self, form):
        response = super(ChatCreateView, self).form_valid(form)

        user = self.request.user
        password = self.request.POST['password']
        if user.is_authenticated and self.request.POST.get('save_to_list') and user.check_password(password):
            self._save_encrypted_list_of_chats(password)
        return response

    def _save_encrypted_list_of_chats(self, password):
        user = self.request.user
        users_chat_list, created = UserChatList.objects.get_or_create(user=user)
        decrypt = UserChatList.decrypt(password, users_chat_list.chat_list)
        dict_data = json.loads(decrypt.decode("utf-8")) if users_chat_list.chat_list else {'chats': []}
        dict_data['chats'].append(self.object.hash)
        json_data = json.dumps(dict_data)
        users_chat_list.chat_list = UserChatList.encrypt(password, json_data)
        users_chat_list.save()


class ChatListView(PermissionRequiredMixin, ListView):
    permission_required = 'is_staff'

    model = models.Chat
    template_name = 'list.html'

    def get_queryset(self):
        queryset = super(ChatListView, self).get_queryset()
        return queryset.order_by('-unread', '-created')


class ChatRespondView(PermissionRequiredMixin, DetailView):
    """
    Chat respond view for staff responses
    """
    permission_required = 'is_staff'

    model = models.Chat

    template_name = 'chat-respond.html'

    slug_field = 'hash'
    slug_url_kwarg = 'hash'

    respond_form = MessageRespondForm
    object = None

    def get_queryset(self):
        """
        Returns chat with messages prefetched
        :return:
        """
        return super(ChatRespondView, self).get_queryset().prefetch_related('message_set')

    def get_context_data(self, **kwargs):
        """
        Puts respond form to the context
        :param kwargs:
        :return:
        """
        self.object = self.get_object()
        context = super(ChatRespondView, self).get_context_data(**kwargs)
        context['form'] = self.respond_form()
        return context

    def get(self, *args, **kwargs):
        """
        Returns chat response and marks chat as read
        :param args:
        :param kwargs:
        :return:
        """
        response = super(ChatRespondView, self).get(*args, **kwargs)
        obj = self.get_object()
        obj.unread = False
        obj.save()
        return response

    def post(self, request, *args, **kwargs):
        """
        Posts new RESPONSE to chat
        :param request:
        :return:
        """
        message = self.respond_form(request.POST)
        if message.is_valid:
            message_instance = message.save(commit=False)
            message_instance.chat = self.get_object()
            message_instance.sender = config.CHAT_RESPONDENT
            message_instance.save()
        return redirect('chat-respond', hash=self.get_object().hash)


class ChatDetailView(SingleObjectMixin, FormView):
    """
    User chat view
    GET: renders authorization form
    POST: with correct password renders chat page with all the messages and new message form
    """
    model = models.Chat
    message_form = MessageForm
    login_form = ChatLoginForm

    template_chat_name = 'chat.html'
    template_login_name = 'chat-login.html'

    slug_field = 'hash'
    slug_url_kwarg = 'hash'

    object = None
    request = None

    def get(self, request, *args, **kwargs):
        """
        Renders authorization form
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.object = self.get_object()

        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        """
        Renders chat if password is correct,
        otherwise renders login form.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not self.has_access():
            return self.proceed_access_fail(request)

        if request.POST.get('from') == 'chat':
            return self.proceed_new_message(request)
        return self.render_to_response(context=self.get_context_data(form=self.message_form()))

    def has_access(self):
        """
        Validates chat password
        :return:
        """
        if not self.object:
            self.object = self.get_object()
        password_hash = hashlib.md5(self.request.POST['password'].encode('utf-8')).hexdigest()
        return self.object.password_hash == password_hash

    def get_form_class(self):
        """
        Return login form for GET and message form for POST
        :return: form
        """
        if self.request.method == 'POST' and self.has_access():
            return self.message_form
        return self.login_form

    def get_template_names(self):
        """
        Return login template for GET and message template for POST
        :return: [template_name]
        """
        if self.request.method == 'POST' and self.has_access():
            return [self.template_chat_name]
        return [self.template_login_name]

    def proceed_access_fail(self, request):
        """
        Renders password fail login
        :param request:
        :return:
        """
        form = self.login_form(request.POST)
        form.add_error(field='password', error='Wrong password')
        return self.render_to_response(context=self.get_context_data(form=form))

    def proceed_new_message(self, request):
        """
        Proceeds new message from user, will mark just unread in case of new message
        :param request:
        :return:
        """
        message = self.message_form(request.POST)
        obj = self.get_object()

        if message.is_valid and not obj.message_set.filter(message=message.data['message']).exists():
            message_instance = message.save(commit=False)
            message_instance.chat = obj
            message_instance.sender = config.CHAT_OWNER
            message_instance.save()
            obj.unread = True
            obj.save()
            return self.render_to_response(context=self.get_context_data(form=self.message_form()))
        return self.render_to_response(context=self.get_context_data())

    def get_queryset(self):
        """
        Return chat with messages prefetched
        :return:
        """
        return super(ChatDetailView, self).get_queryset().prefetch_related('message_set')

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        ctx = super(ChatDetailView, self).get_context_data(**kwargs)
        encrypt_list, created = UserChatList.objects.get_or_create(user=self.request.user)
        chat_list = encrypt_list.chat_list
        password = self.request.POST.get('password')
        if chat_list and password and self.request.user.check_password(self.request.POST['password']):
            decrypt = UserChatList.decrypt(password, chat_list)
            try:
                ctx['chat_list'] = json.loads(decrypt.decode("utf-8"))
            except:
                ctx['chat_list'] = 'Cannot unpack your list'
        return ctx
