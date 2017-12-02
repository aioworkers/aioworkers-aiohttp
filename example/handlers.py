
async def status(request):
    """
    ---
    tags: [system]
    responses:
      default:
        description: ok
    """
    return request.app.context.config.status
