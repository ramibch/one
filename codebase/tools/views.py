from django.http import Http404, HttpResponse
from django.shortcuts import render

from codebase.base.utils.telegram import Bot

from .tools import TOOL_LISTING_OBJECT, TOOLS, get_related_tools, get_tool


def tool_index(request):
    context = {"object": TOOL_LISTING_OBJECT, "tools": TOOLS}
    return render(request, "tools/tool_index.html", context)


def tool_detail(request, slug):
    tool = get_tool(slug)
    if tool is None:
        raise Http404
    if request.method == "POST":
        if not tool.form:
            obj = tool.process_func()
            return render(request, tool.results_template, {"self": obj})
        form = tool.form(request.POST)
        if form.is_valid():
            obj = form.save()
            try:
                obj.process()
            except Exception as e:
                Bot.to_admin(f"Tool error: {tool.slug}\n{str(e)}")
                return HttpResponse(e)
            return render(request, tool.results_template, {"self": obj})
        else:
            return HttpResponse(form.errors.as_ul())
    context = {"object": tool, "related_tools": get_related_tools(tool)}
    return render(request, tool.detail_template, context)
