
# Dark Ages Wiki Styled Django Application Guide

## Project Overview

This comprehensive guide outlines best practices for developing scalable web applications using Python and Django. It emphasizes clear, technical implementation with precise Django examples, leveraging Django's built-in features and tools for maximum efficiency. The guide prioritizes readability, maintainability, and follows Django's coding style guide with PEP 8 compliance.

This aims to create a structured Wiki style website for the 1999 Nexon (now KRU Interactive) video game found at https://www.darkages.com/. Utilizing an entirely classic Django MVT style with almost all of the rendering being done on the backend. Much of the information will initially come from vorlof.com and credit "Vorlof" for all the information.

## Tech Stack

- **Backend Framework**: Django 4.2+ with Python 3.9+
- **Database**: PostgreSQL, SQLite (development)
- **Caching**: Memcached
- **CSS Framework**: Tailwind
- **Testing**: Django unittest + pytest-django
- **Static Files**: WhiteNoise or CDN integration
- **Security**: Django's built-in security features

## Project Structure

```
darkagesWiki/
├── manage.py
├── pyprojectject.toml 
├── README.md 
├── darkagesWiki/
│   ├── __init__.py
│   ├── _local_settings.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── wiki/
│   ├── __init__.py
│   ├── admin.py
│   ├── forms.py
│   ├── urls.py
│   ├── functions.py
│   ├── model_constants.py
│   ├── models.py
│   ├── urls.py
│   ├── tests.py
│   └── views.py
├── requirements.txt
├── static/
├── media/
├── templates/
│   └── base/
├── locale/
└── tests/
```

## Development Guidelines

### Key Principles

- Write clear, technical responses with precise Django examples
- Use Django's built-in features and tools wherever possible to leverage its full capabilities
- Prioritize readability and maintainability; follow Django's coding style guide (PEP 8 compliance)
- Use descriptive variable and function names; adhere to naming conventions
- Structure your project in a modular way using Django apps to promote reusability and separation of concerns

### Django/Python Best Practices

#### Views and URL Patterns

- Use Django's class-based views (CBVs) for more complex views; prefer function-based views (FBVs) for simpler logic
- Follow the MVT (Model-View-Template) pattern strictly for clear separation of concerns
- Use Django's URL dispatcher (urls.py) to define clear and RESTful URL patterns

```python
# views.py - Function-based view for simple logic
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Article

@require_http_methods(["GET"])
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id, is_published=True)
    return render(request, 'articles/detail.html', {'article': article})

# views.py - Class-based view for complex logic
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        return Article.objects.filter(
            is_published=True
        ).select_related('author').order_by('-created_at')

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content', 'category']
    template_name = 'articles/create.html'
    success_url = reverse_lazy('articles:list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
```

#### Models and Database

- Leverage Django's ORM for database interactions; avoid raw SQL queries unless necessary for performance
- Keep business logic in models and forms; keep views light and focused on request handling

```python
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class TimestampedModel(models.Model):
    """Abstract base class with timestamp fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(TimestampedModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Article(TimestampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    content = models.TextField()
    excerpt = models.TextField(max_length=300, blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_published', '-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_recent(self):
        return (timezone.now() - self.created_at).days < 7
```

#### Forms and Validation

- Utilize Django's form and model form classes for form handling and validation
- Use Django's validation framework to validate form and model data

```python
# forms.py
from django import forms
from django.core.exceptions import ValidationError
from .models import Article, Category

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'content', 'excerpt', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
            'excerpt': forms.Textarea(attrs={'rows': 3, 'cols': 80}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError("Title must be at least 5 characters long.")
        return title

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        excerpt = cleaned_data.get('excerpt')

        if content and len(content) < 100:
            raise ValidationError("Content must be at least 100 characters long.")

        if not excerpt and content:
            # Auto-generate excerpt if not provided
            cleaned_data['excerpt'] = content[:297] + '...' if len(content) > 300 else content

        return cleaned_data

    def save(self, commit=True):
        article = super().save(commit=False)
        if self.user:
            article.author = self.user
        if commit:
            article.save()
        return article
```

## Environment Setup

### Development Requirements

- Python >= 3.9
- Django >= 4.2
- PostgreSQL >= 12 (production) or SQLite (development)

### Installation Steps

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements/development.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# 4. Run database migrations
python manage.py migrate

# 5. Create superuser
python manage.py createsuperuser

# 6. Collect static files
python manage.py collectstatic

# 7. Run development server
python manage.py runserver
```

### Environment Variables Configuration

```env
# .env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

## Core Feature Implementation

### Authentication and User Management

```python
# Use Django's built-in user model and authentication framework
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Custom user profile model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# API authentication views
@api_view(['POST'])
def api_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username and password:
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.id,
                'username': user.username
            })

    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Successfully logged out'})
    except:
        return Response({'error': 'Error logging out'}, status=status.HTTP_400_BAD_REQUEST)
```

### Middleware Implementation

```python
# middleware.py
import logging
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from django.core.cache import cache
import time

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware to log all requests"""

    def process_request(self, request):
        request.start_time = time.time()
        logger.info(f"Request started: {request.method} {request.path}")

    def process_response(self, request, response):
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time
            logger.info(
                f"Request completed: {request.method} {request.path} "
                f"- Status: {response.status_code} - Duration: {duration:.2f}s"
            )
        return response

class RateLimitMiddleware(MiddlewareMixin):
    """Simple rate limiting middleware"""

    def process_request(self, request):
        if request.path.startswith('/api/'):
            client_ip = self.get_client_ip(request)
            cache_key = f"rate_limit_{client_ip}"

            requests_count = cache.get(cache_key, 0)
            if requests_count >= 100:  # 100 requests per minute
                return JsonResponse(
                    {'error': 'Rate limit exceeded'},
                    status=429
                )

            cache.set(cache_key, requests_count + 1, 60)  # 1 minute timeout

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
```

## Error Handling and Validation

### Django Error Handling

```python
# error_handlers.py
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
import logging

logger = logging.getLogger(__name__)

@requires_csrf_token
def handler404(request, exception):
    """Custom 404 error handler"""
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Not Found',
            'message': 'The requested resource was not found.',
            'status_code': 404
        }, status=404)

    return render(request, 'errors/404.html', {
        'exception': str(exception)
    }, status=404)

@requires_csrf_token
def handler500(request):
    """Custom 500 error handler"""
    logger.error(f"Server error on {request.path}", exc_info=True)

    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred.',
            'status_code': 500
        }, status=500)

    return render(request, 'errors/500.html', status=500)

# Custom exception handling in views
from django.core.exceptions import ValidationError, PermissionDenied
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    """Custom DRF exception handler"""
    response = exception_handler(exc, context)

    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'An error occurred',
            'details': response.data,
            'status_code': response.status_code
        }
        response.data = custom_response_data

    return response

# View-level error handling
from django.db import transaction
from django.contrib import messages

def create_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, user=request.user)
        try:
            with transaction.atomic():
                if form.is_valid():
                    article = form.save()
                    messages.success(request, f'Article "{article.title}" created successfully!')
                    return redirect('articles:detail', slug=article.slug)
                else:
                    messages.error(request, 'Please correct the errors below.')
        except ValidationError as e:
            messages.error(request, f'Validation error: {e.message}')
        except Exception as e:
            logger.error(f"Unexpected error creating article: {str(e)}", exc_info=True)
            messages.error(request, 'An unexpected error occurred. Please try again.')
    else:
        form = ArticleForm()

    return render(request, 'articles/create.html', {'form': form})
```

### Model and Form Validation

```python
# Custom validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_file_size(value):
    """Validate uploaded file size"""
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError(_("File size cannot exceed 5MB."))

def validate_slug_format(value):
    """Validate slug format"""
    import re
    if not re.match(r'^[a-z0-9-]+$', value):
        raise ValidationError(_("Slug can only contain lowercase letters, numbers, and hyphens."))

# Enhanced model with validation
class Article(TimestampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, validators=[validate_slug_format])
    featured_image = models.ImageField(
        upload_to='articles/',
        blank=True,
        null=True,
        validators=[validate_file_size]
    )

    def clean(self):
        """Model-level validation"""
        super().clean()
        if self.is_published and not self.content:
            raise ValidationError(_("Published articles must have content."))

        if self.published_at and self.published_at > timezone.now():
            raise ValidationError(_("Published date cannot be in the future."))

    def save(self, *args, **kwargs):
        self.full_clean()  # Run model validation
        super().save(*args, **kwargs)
```

## Performance Optimization

### Database Query Optimization

```python
# Optimized querysets using select_related and prefetch_related
from django.db.models import Prefetch, Count, Q

class OptimizedArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        """Optimized queryset with proper joins"""
        return Article.objects.select_related(
            'author', 'category'
        ).prefetch_related(
            'tags',
            Prefetch(
                'comments',
                queryset=Comment.objects.select_related('author').filter(is_approved=True)
            )
        ).annotate(
            comments_count=Count('comments', filter=Q(comments__is_approved=True))
        )

# Database indexing example
class Article(TimestampedModel):
    class Meta:
        indexes = [
            models.Index(fields=['is_published', '-created_at']),
            models.Index(fields=['category', '-published_at']),
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['slug']),  # For URL lookups
        ]

# Custom manager for common queries
class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def recent(self, days=7):
        cutoff_date = timezone.now() - timedelta(days=days)
        return self.get_queryset().filter(published_at__gte=cutoff_date)

    def by_category(self, category_slug):
        return self.get_queryset().filter(category__slug=category_slug)

class Article(TimestampedModel):
    # ... fields ...

    objects = models.Manager()  # Default manager
    published = PublishedArticleManager()  # Custom manager
```

## Security Considerations

### Django Security Best Practices

```python
# settings/security.py
import os

# CSRF Protection
CSRF_COOKIE_SECURE = True  # Only send CSRF cookie over HTTPS
CSRF_COOKIE_HTTPONLY = True  # Prevent JavaScript access to CSRF cookie
CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']

# Session Security
SESSION_COOKIE_SECURE = True  # Only send session cookie over HTTPS
SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript access to session cookie
SESSION_COOKIE_AGE = 3600  # 1 hour session timeout
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SQL Injection Protection (built-in with Django ORM)
# XSS Prevention (built-in with Django templates)

# Custom security middleware
class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Add security headers
        response['X-Frame-Options'] = 'DENY'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

        return response

# Input validation and sanitization
from django.utils.html import escape
from django.core.validators import validate_email

def sanitize_user_input(data):
    """Sanitize user input to prevent XSS"""
    if isinstance(data, str):
        return escape(data)
    elif isinstance(data, dict):
        return {key: sanitize_user_input(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_user_input(item) for item in data]
    return data
```

### Authentication and Authorization

```python
# Custom permission classes
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    """Custom permission to only allow owners to edit objects"""

    def has_object_permission(self, request, view, obj):
        # Read permissions for any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions only to the owner
        return obj.author == request.user

class IsStaffOrReadOnly(BasePermission):
    """Allow staff users to modify, others read-only"""

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.is_staff

# Rate limiting for API endpoints
from django.core.cache import cache
from rest_framework.throttling import UserRateThrottle

class CustomUserRateThrottle(UserRateThrottle):
    scope = 'user'

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            ident = request.user.pk
        else:
            ident = self.get_ident(request)

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
```

## Testing Strategy

### Unit Testing with Django

```python
# tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.articles.models import Article, Category

class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_article_creation(self):
        """Test article creation with valid data"""
        article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            author=self.user,
            category=self.category,
            content='This is test content for the article.',
            is_published=True
        )

        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.author, self.user)
        self.assertTrue(article.is_published)
        self.assertIsNotNone(article.published_at)

    def test_article_str_representation(self):
        """Test string representation of article"""
        article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            author=self.user,
            category=self.category,
            content='Test content'
        )
        self.assertEqual(str(article), 'Test Article')

    def test_article_validation(self):
        """Test article model validation"""
        article = Article(
            title='Test Article',
            slug='test-article',
            author=self.user,
            category=self.category,
            content='',  # Empty content
            is_published=True  # Published but no content
        )

        with self.assertRaises(ValidationError):
            article.full_clean()

# tests/test_views.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class ArticleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_article_list_view(self):
        """Test article list view"""
        # Create test articles
        Article.objects.create(
            title='Published Article',
            slug='published-article',
            author=self.user,
            category=self.category,
            content='Test content',
            is_published=True
        )

        response = self.client.get(reverse('articles:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Published Article')

    def test_article_detail_view(self):
        """Test article detail view"""
        article = Article.objects.create(
            title='Test Article',
            slug='test-article',
            author=self.user,
            category=self.category,
            content='Test content',
            is_published=True
        )

        response = self.client.get(
            reverse('articles:detail', kwargs={'slug': article.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, article.title)

class ArticleAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_create_article_authenticated(self):
        """Test creating article with authenticated user"""
        self.client.force_authenticate(user=self.user)

        data = {
            'title': 'New Article',
            'category_id': self.category.id,
            'content': 'This is new article content.',
            'is_published': True
        }

        response = self.client.post('/api/articles/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)

    def test_create_article_unauthenticated(self):
        """Test creating article without authentication"""
        data = {
            'title': 'New Article',
            'category_id': self.category.id,
            'content': 'This is new article content.'
        }

        response = self.client.post('/api/articles/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

### Integration Testing

```python
# tests/test_integration.py
from django.test import TransactionTestCase
from django.db import transaction
from django.contrib.auth.models import User
from apps.articles.models import Article, Category
from apps.articles.tasks import send_notification_email

class ArticleIntegrationTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )

    def test_article_publication_workflow(self):
        """Test complete article publication workflow"""
        # Create draft article
        article = Article.objects.create(
            title='Draft Article',
            slug='draft-article',
            author=self.user,
            category=self.category,
            content='This is a draft article.',
            is_published=False
        )

        self.assertFalse(article.is_published)
        self.assertIsNone(article.published_at)

        # Publish article
        article.is_published = True
        article.save()

        self.assertTrue(article.is_published)
        self.assertIsNotNone(article.published_at)

        # Verify signal was triggered (mock in real tests)
        # This would trigger send_notification_email task
```

## Deployment Guide

## Common Issues

### Issue 1: Database Connection Errors

**Solution**:

- Check database credentials and connection settings
- Ensure database server is running and accessible
- Verify firewall settings and network connectivity
- Use connection pooling for production environments

### Issue 2: Static Files Not Loading

**Solution**:

- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` settings
- Ensure web server is configured to serve static files
- Use CDN for production static file serving

### Issue 3: Celery Tasks Not Executing

**Solution**:

- Verify Redis/RabbitMQ broker is running
- Check Celery worker processes are active
- Ensure task routing and queue configuration is correct
- Monitor Celery logs for error messages

### Issue 4: Performance Issues with Large Datasets

**Solution**:

- Implement database query optimization with `select_related` and `prefetch_related`
- Add appropriate database indexes
- Use pagination for large result sets
- Implement caching strategies

## Reference Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [Django Security Best Practices](https://docs.djangoproject.com/en/stable/topics/security/)
- [Django Performance Optimization](https://docs.djangoproject.com/en/stable/topics/performance/)
- [Python PEP 8 Style Guide](https://pep8.org/)
- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)

## Changelog

### v1.0.0 (2024-12-19)

- Initial release of Python Django scalable web application development guide
- Comprehensive coverage of Django best practices and patterns
- Included examples for models, views, forms, and API development
- Added performance optimization and security considerations
- Covered testing strategies and deployment guidelines

---

**Note**: This guide is based on Django 4.2+ and Python 3.9+. Please adjust configurations and examples according to your specific project requirements and the versions you are using. Always refer to the official Django documentation for the most up-to-date information.

