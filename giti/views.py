from giti.utils import get_repo_or_404, get_blob_or_404, get_tree_or_404,\
        get_all_repositories
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from git import IndexEntry

def tree_show(request, repo_name, path=None):
    repo = get_repo_or_404(repo_name)
    git_repo = repo.get_git_repo()
    commit = git_repo.head.commit
    tree = get_tree_or_404(commit, path)
    return render_to_response('giti/tree_show.html',
            {'commit': commit, 'tree': tree, 'repo': repo},
            RequestContext(request))

def edit(request, repo_name, path):
    repo = get_repo_or_404(repo_name)
    git_repo = repo.get_git_repo()
    commit = git_repo.head.commit
    blob = get_blob_or_404(commit, path)
    return render_to_response('giti/blob_edit.html',
            {'commit': commit, 'blob': blob, 'repo': repo},
            RequestContext(request))

def raw(request, repo_name, path):
    repo = get_repo_or_404(repo_name)
    git_repo = repo.get_git_repo()
    commit = git_repo.head.commit
    blob = get_blob_or_404(commit, path)
    return HttpResponse(blob.data_stream.read(), mimetype=blob.mime_type)

def show(request, repo_name, path):
    repo = get_repo_or_404(repo_name)
    git_repo = repo.get_git_repo()
    commit = git_repo.head.commit
    blob = get_blob_or_404(commit, path)
    return render_to_response('giti/blob_show.html',
            {'commit': commit, 'blob': blob, 'repo': repo},
            RequestContext(request))

def stage(request, repo_name, path):
    assert request.method == 'POST' and request.POST.has_key('data')
    repo = get_repo_or_404(repo_name)
    git_repo = repo.get_git_repo()
    commit = git_repo.head.commit
    blob = get_blob_or_404(commit, path)
    repo.index_store(blob.path, request.POST['data'], blob.mode)
    return redirect('giti.views.show', repo_name=repo_name, path=blob.path)

def delete(request, repo_name, path):
    repo = get_repo_or_404(repo_name)
    git_repo = repo.get_git_repo()
    commit = git_repo.head.commit
    blob = get_blob_or_404(commit, path)
    repo.index_delete(blob.path)
    return redirect('giti.views.edit', repo_name=repo_name, path=blob.path)


def repository_list(request):
    return render_to_response('giti/repository_list.html',
            {'object_list': get_all_repositories() },
            RequestContext(request))

# Functionality for the index

def index_commit(request, repo_name):
    """Commit all currently staged changes"""
    repo = get_repo_or_404(repo_name)
    git_repo = repo.get_git_repo()
    if request.method == 'POST':
        git_repo.index.commit(request.POST['commit_msg'])
        return redirect('giti.views.tree_show', repo_name=repo.name, 
                path='')
    else:
        return render_to_response('giti/index_commit.html',
            {'repo': repo},
            RequestContext(request))

def index_revert(request, repo_name):
    """Reset the current index by reverting all staged changes"""
    repo = get_repo_or_404(repo_name)
    git_repo = repo.get_git_repo()
    git_repo.index.reset()
    return redirect('giti.views.tree_show', repo_name=repo.name, path='')

def index_remove(request, repo_name, path):
    """Purge all staged changes to a path"""
    return redirect('giti.views.tree_show', repo_name=repo.name, path='')
