from functools import wraps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

def paginate_results(page_size=10):
    """
    Decorator to add pagination to a Django view.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Call the original view function to get the data
            data = view_func(request, *args, **kwargs)

            # Ensure the view returns a queryset or list
            if not isinstance(data, list):
                return JsonResponse({"error": "View must return a list or queryset"}, status=400)

            # Get pagination parameters from the request
            page = request.GET.get('page', 1)
            custom_page_size = request.GET.get('page_size', page_size)

            try:
                # Create the paginator
                paginator = Paginator(data, custom_page_size)
                paginated_data = paginator.page(page)
            except PageNotAnInteger:
                return JsonResponse({"error": "Invalid page number"}, status=400)
            except EmptyPage:
                return JsonResponse({"error": "Page out of range"}, status=404)

            # Create the paginated response
            response = {
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": paginated_data.number,
                "next_page": paginated_data.next_page_number() if paginated_data.has_next() else None,
                "previous_page": paginated_data.previous_page_number() if paginated_data.has_previous() else None,
                "results": list(paginated_data),
            }

            return JsonResponse(response)
        return wrapper
    return decorator
