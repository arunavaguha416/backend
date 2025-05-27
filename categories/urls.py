from categories.views.category_view import *
from django.urls import path
urlpatterns = [
    path('add/', CategoryAdd.as_view(), name='category-add'),
    path('list/', CategoryList.as_view(), name='category-list'),
    path('published/', PublishedCategoryList.as_view(), name='category-published-list'),
    path('deleted/', DeletedCategoryList.as_view(), name='category-deleted-list'),
    path('details/', CategoryDetails.as_view(), name='category-details'),
    path('update/', CategoryUpdate.as_view(), name='category-update'),
    path('publish/', ChangeCategoryPublishStatus.as_view(), name='category-publish'),
    path('delete/<int:category_id>/', CategoryDelete.as_view(), name='category-delete'),
    path('restore/', RestoreCategory.as_view(), name='category-restore'),
    path('loadCategory/', LoadCategoriesView.as_view(), name='load-category'),
]