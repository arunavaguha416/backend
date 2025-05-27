from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.db.models import Q
from categories.serializers.category_serializer import *
from categories.models.category import Category
from django.core.paginator import Paginator
import datetime
import json
from django.conf import settings
class CategoryAdd(APIView):
    """
    API View for adding a new category. Only accessible by admin users.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request):
        """
        Handle POST request to add a new category.
        """
        try:
            # Attempt to serialize and save the new category data
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)  # Associate with the current user
                return Response({
                    'status': True,
                    'message': 'Category added successfully',
                    'records': serializer.data
                }, status=status.HTTP_200_OK)

            # Return error if data is invalid
            return Response({
                'status': False,
                'message': 'Invalid data',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': 'An error occurred while adding the category',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class CategoryList(APIView):
    """
    API View for listing categories. Accessible by admin users.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request):
        """
        Handle POST request to list categories with optional filtering.
        """
        try:
            # Apply filtering (e.g., by title)
            title_filter = request.data.get('title', None)
            categories = Category.objects.filter(deleted_at__isnull=True)  # Exclude soft-deleted categories

            if title_filter:
                categories = categories.filter(title__icontains=title_filter)

            # Order categories by created_at (descending)
            categories = categories.order_by('-created_at')

            # Check if any categories were found
            if categories.exists():
                # Serialize the data
                serializer = CategorySerializer(categories, many=True)

                return Response({
                    'status': True,
                    'records': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                # If no categories found
                return Response({
                    'status': False,
                    'message': 'Categories not found',
                }, status=status.HTTP_200_OK)

        except Exception as error:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
class PublishedCategoryList(APIView):
    """
    API View for listing categories. Accessible by any users.
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        Handle GET request to list all published categories.
        """
        try:
            # Fetch categories based on the query
            categories = Category.objects.filter(
                published_at__isnull=False,
                user=request.user if request.user.is_authenticated else None
            ).values('id', 'title').order_by('-created_at')

            # Check if any categories were found
            if categories.exists():
                return Response({
                    'status': True,
                    'records': categories
                }, status=status.HTTP_200_OK)

            else:
                # If no categories found
                return Response({
                    'status': False,
                    'message': 'Categories not found',
                }, status=status.HTTP_200_OK)

        except Exception as error:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

class DeletedCategoryList(APIView):
    """
    API View for listing of deleted categories. Accessible by admin users.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request):
        """
        Handle POST request to list deleted categories with optional filtering and pagination.
        """
        try:
            # Extract search parameters from request data
            search_data = request.data
            page = search_data.get('page')
            page_size = search_data.get('page_size', 10)
            search_title = search_data.get('title', '')
            search_description = search_data.get('description', '')

            # Build query based on search parameters
            query = Q(deleted_at__isnull=False, user=request.user)  # Filter deleted categories for the user
            if search_title:
                query &= Q(title__icontains=search_title)
            if search_description:
                query &= Q(description__icontains=search_description)

            # Fetch categories based on the query
            categories = Category.objects.filter(query).order_by('-created_at')

            # Check if any categories were found
            if categories.exists():
                # Handle pagination if page parameter is provided
                if page is not None:
                    paginator = Paginator(categories, page_size)
                    paginated_categories = paginator.get_page(page)
                    serializer = CategorySerializer(paginated_categories, many=True)

                    return Response({
                        'status': True,
                        'count': paginator.count,
                        'num_pages': paginator.num_pages,
                        'records': serializer.data
                    }, status=status.HTTP_200_OK)
                else:
                    # Return all categories if no pagination is requested
                    serializer = CategorySerializer(categories, many=True)
                    return Response({
                        'status': True,
                        'count': categories.count(),
                        'records': serializer.data
                    }, status=status.HTTP_200_OK)

            else:
                # If no categories found
                return Response({
                    'status': False,
                    'message': 'Categories not found',
                }, status=status.HTTP_200_OK)

        except Exception as error:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetails(APIView):
    """
    API View for retrieving details of a specific category. Only accessible by admin users.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request):
        """
        Handle POST request to get details of a specific category.
        """
        try:
            category_id = request.data.get('id')

            # Fetch specific category details if an ID is provided
            if category_id:
                # Get category details based on category ID
                category = Category.objects.filter(id=category_id, user=request.user).values('id', 'title', 'description').first()

                if category:
                    # If category found
                    return Response({
                        'status': True,
                        'records': category
                    }, status=status.HTTP_200_OK)

                else:
                    # If no category found
                    return Response({
                        'status': False,
                        'message': 'Category not found',
                    }, status=status.HTTP_200_OK)

            else:
                # If no category ID provided
                return Response({
                    'status': False,
                    'message': 'Please provide categoryId'
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': 'An error occurred while fetching category details',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class CategoryUpdate(APIView):
    """
    API View for updating an existing category. Only accessible by admin users.
    """
    permission_classes = (IsAdminUser,)

    def put(self, request):
        """
        Handle PUT request to update a category.
        """
        try:
            category_id = request.data.get('id')

            # Get first data from category by ID
            category = Category.objects.filter(id=category_id, user=request.user).first()

            if category:
                # For the particular category, update requested data
                serializer = CategorySerializer(category, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        'status': True,
                        'message': 'Category updated successfully'
                    }, status=status.HTTP_200_OK)

                return Response({
                    'status': False,
                    'message': 'Invalid data',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': False,
                'message': 'Category not found'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': 'An error occurred while updating the category',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

class ChangeCategoryPublishStatus(APIView):
    """
    API View for changing the publish status of a category. Only accessible by admin users.
    """
    permission_classes = (IsAdminUser,)

    def put(self, request):
        """
        Handle PUT request to change the publish status of a category.
        """
        try:
            category_id = request.data.get('id')
            publish = request.data.get('status')

            # If requested flag is 1 then set publish timestamp
            if publish == 1:
                data = {'published_at': datetime.datetime.now()}
            # If requested flag is 0 then unpublish category
            elif publish == 0:
                data = {'published_at': None}
            else:
                return Response({
                    'status': False,
                    'message': 'Invalid status value. Use 1 to publish or 0 to unpublish.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Fetch category by ID
            category = Category.objects.filter(id=category_id, user=request.user).first()
            if not category:
                return Response({
                    'status': False,
                    'message': 'Category not found'
                }, status=status.HTTP_200_OK)

            serializer = CategorySerializer(category, data=data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'message': 'Publish status updated successfully',
                }, status=status.HTTP_200_OK)

            return Response({
                'status': False,
                'message': 'Unable to update publish status',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
            # Handle any unexpected errors
            return Response({
                'status': False,
                'message': str(error),
            }, status=status.HTTP_400_BAD_REQUEST)

class CategoryDelete(APIView):
    """
    API View for deleting a category. Only accessible by admin users.
    """
    permission_classes = (IsAdminUser,)

    def delete(self, request, category_id):
        try:
            # Try to fetch the category with the given ID
            category = Category.objects.filter(id=category_id, user=request.user).first()

            if category:
                # If record found then perform soft delete
                category.soft_delete()
                return Response({
                    'status': True,
                    'message': 'Category deleted successfully'
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'status': False,
                    'message': 'Category not found'
                }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

class RestoreCategory(APIView):
    """
    API View for restoring a category. Only accessible by admin users.
    """
    permission_classes = (IsAdminUser,)

    def post(self, request):
        try:
            # Get ID from request
            category_id = request.data.get('id')

            # Fetch record to check availability
            category = Category.objects.filter(id=category_id, user=request.user).first()

            if category:
                # Set deleted_at to null
                category.deleted_at = None
                category.save()
                return Response({
                    'status': True,
                    'message': 'Category restored successfully'
                }, status=status.HTTP_200_OK)

            else:
                # Check if the category exists
                return Response({
                    'status': False,
                    'message': 'Category not found'
                }, status=status.HTTP_200_OK)

        except Exception as error:
            return Response({
                'status': False,
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)
        
class LoadCategoriesView(APIView):
    """
    API View to load categories from categorySeed.json. Accessible only by admin users.
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Handle POST request to load categories from categorySeed.json.
        """
        try:
            # Path to categorySeed.json (in BACKEND/)
            json_path = settings.BASE_DIR / 'categorySeed.json'

            # Read the JSON file
            with open(json_path, 'r') as file:
                categories_data = json.load(file)

            # Process each category entry
            created_categories = []
            for category_data in categories_data:
                # Verify the model name
                if category_data.get('model') != 'categories.category':
                    continue

                # Extract fields
                fields = category_data.get('fields', {})
                pk = category_data.get('pk')

                # Check if category already exists
                if Category.objects.filter(id=pk).exists():
                    continue

                # Prepare data for creation
                category_dict = {
                    'id': pk,
                    'title': fields.get('title'),
                    'description': fields.get('description', ''),
                    'published_at': fields.get('published_at'),
                    'deleted_at': fields.get('deleted_at')
                }

                # Create the category
                serializer = CategorySerializer(data=category_dict)
                if serializer.is_valid():
                    serializer.save()
                    created_categories.append(serializer.data)
                else:
                    return Response({
                        'status': False,
                        'message': 'Invalid category data',
                        'errors': serializer.errors
                    }, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                'status': True,
                'message': f'Successfully loaded {len(created_categories)} categories',
                'categories': created_categories
            }, status=status.HTTP_201_CREATED)

        except FileNotFoundError:
            return Response({
                'status': False,
                'message': 'categorySeed.json file not found'
            }, status=status.HTTP_400_BAD_REQUEST)

        except json.JSONDecodeError:
            return Response({
                'status': False,
                'message': 'Invalid JSON format in categorySeed.json'
            }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({
                'status': False,
                'message': 'An error occurred while loading categories',
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)