from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import CustomUser
from core.models import Answer, Question, Comment


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
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'firstName', 'lastName',)


class UserDetailSerializer(serializers.ModelSerializer):

    questions = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()
    followers = serializers.StringRelatedField(many=True, read_only=True)
    following = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id', 'firstName', 'lastName', 'questions', 'answers', 'followers', 'following',)

    def get_questions(self, instance):
        questions = Question.objects.filter(author=instance)
        return QuestionSerializer(questions, many=True).data
    
    def get_answers(self, instance):
        answers = Answer.objects.filter(author=instance)
        return AnswerSerializer(answers, many=True).data
    

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

    class Meta:
        model = Answer
        exclude = ["id", "question", "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_question_slug(self, instance):
        return instance.question.slug
    
    def get_comments(self, instance):
        comments = Comment.objects.filter(answer=instance)
        return CommentSerializer(comments, many=True).data
    
    def get_upvoted_users(self, instance):
        return instance.upvotes.all().values_list('username', flat=True)
    
    def get_downvoted_users(self, instance):
        return instance.downvotes.all().values_list('username', flat=True)


class QuestionSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    answers_count = serializers.SerializerMethodField()
    answers = AnswerSerializer(many=True, read_only=True)
    upvoted_users = serializers.SerializerMethodField()
    downvoted_users = serializers.SerializerMethodField()

    class Meta:
        model = Question
        exclude = ["id", "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")

    def get_answers_count(self, instance):
        return instance.answers.count()
    
    def get_answers(self, instance):
        return AnswerSerializer(instance.answers.all(), many=True).data
    
    def get_upvoted_users(self, instance):
        return instance.upvotes.all().values_list('username', flat=True)
    
    def get_downvoted_users(self, instance):
        return instance.downvotes.all().values_list('username', flat=True)
    
    

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ["id", "updated_at"]
        read_only_fields = ["author", "answer"]

    def get_created_at(self, instance):
        return instance.created_at.strftime("%B %d, %Y")
    

