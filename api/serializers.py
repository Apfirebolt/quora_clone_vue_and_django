from rest_framework import serializers
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import CustomUser
from accounts.documents import CustomUserDocument
from core.models import Answer, Question, Comment, Tag, Notification



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': ('No account exists with these credentials, check password and email')
    }

    def validate(self, attrs):
        
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data 
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['id'] = self.user.id
        data['is_admin'] = self.user.is_superuser
        return data


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        min_length=8,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    access = serializers.SerializerMethodField()
    refresh = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'is_staff', 'password', 'access', 'refresh',)
    
    def get_refresh(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh)

    def get_access(self, user):
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token),
        return access

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class CustomUserDocumentSerializer(DocumentSerializer):
    class Meta:
        document = CustomUserDocument
        fields = (
            'id', 
            'email', 
            'username', 
            'firstName', 
            'lastName',
            'is_staff',
            'is_superuser'
        )
        # Optional: Specify read-only fields if necessary
        read_only_fields = fields
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'firstName', 'lastName', 'profilePicture',)


class UserDetailSerializer(serializers.ModelSerializer):

    questions = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    followers = serializers.StringRelatedField(many=True, read_only=True)
    following = serializers.StringRelatedField(many=True, read_only=True)
    questions_count = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'firstName', 'lastName', 'questions', 'answers', 
                  'followers', 'following', 'profilePicture', 'questions_count', 'answers_count')

    def get_questions(self, instance):
        # Use prefetch_related and select_related to avoid N+1 queries
        questions = instance.questions.all()
        return QuestionSerializer(questions, many=True).data
    
    def get_answers(self, instance):
        # Use prefetch_related and select_related to avoid N+1 queries
        answers = instance.answer_set.all()
        return AnswerSerializer(answers, many=True).data
    
    def get_questions_count(self, instance):
        return getattr(instance, 'questions_count', instance.questions.count())
    
    def get_answers_count(self, instance):
        return getattr(instance, 'answers_count', instance.answer_set.count())
    

class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'is_staff', 'is_superuser')


class AnswerSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()
    question_slug = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    upvoted_by = serializers.StringRelatedField(many=True, read_only=True)
    downvoted_by = serializers.StringRelatedField(many=True, read_only=True)
    upvoted_users = serializers.SerializerMethodField()
    downvoted_users = serializers.SerializerMethodField()
    # Uses annotation for efficiency when available, otherwise performs count query
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        exclude = ["id", "question", "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_question_slug(self, instance):
        return instance.question.slug
    
    def get_comments(self, instance):
        # Use prefetch_related to avoid N+1 queries
        comments = instance.comments.all()
        return CommentSerializer(comments, many=True).data
    
    def get_comments_count(self, instance):
        # Use annotation to avoid additional query
        return getattr(instance, 'comments_count', instance.comments.count())
    
    def get_upvoted_users(self, instance):
        return list(instance.upvotes.all().values_list('username', flat=True))
    
    def get_downvoted_users(self, instance):
        return list(instance.downvotes.all().values_list('username', flat=True))


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    image = serializers.ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    upvoted_users = serializers.SerializerMethodField()
    downvoted_users = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = ["id", "updated_at"]
        read_only_fields = ["uuid", "slug", "author", "image_url"]

    def get_image_url(self, instance):
        if instance.image:
            return instance.image.url
        return None

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_answers_count(self, instance):
        # Use annotation to avoid additional query
        return getattr(instance, "answers_count", instance.answers.count())

    def get_answers(self, instance):
        # Pass context so nested URLs (or request-dependent fields) serialize correctly
        return AnswerSerializer(
            instance.answers.all(), many=True, context=self.context
        ).data

    def get_upvoted_users(self, instance):
        # If prefetch_related('upvotes') is used in the queryset, instance.upvotes.all()
        # uses the prefetch cache without hitting the DB again
        return [user.username for user in instance.upvotes.all()]

    def get_downvoted_users(self, instance):
        # Uses prefetch cache instead of issuing a separate DB query via .values_list()
        return [user.username for user in instance.downvotes.all()]
    
    

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ["id", "updated_at"]
        read_only_fields = ["author", "answer"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")
    

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    recipient = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y %H:%M")
    

