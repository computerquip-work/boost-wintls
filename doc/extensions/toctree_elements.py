from sphinx import addnodes
import docutils.nodes


def html_page_context(app, pagename, templatename, context, doctree):
    if 'toctree' not in context:
        return

    builder = app.builder
    env = builder.env
    doctree = env.get_doctree(env.config.master_doc)

    for node in doctree.traverse(addnodes.toctree):
        toctreenode = node
        break

    toctree = env.resolve_toctree(pagename, builder, toctreenode,
                                  includehidden=True)

    toctree_elements = {}
    for item in toctree.traverse(docutils.nodes.list_item):
        if 'toctree-l1' in item['classes']:

            children = []
            for child in item.traverse(docutils.nodes.list_item,
                                       include_self=False):
                title = child[0].astext()
                for ref in child.traverse(docutils.nodes.reference):
                    link = ref["refuri"]
                    break
                children.append((title, link))
            toctree_elements[item[0].astext()] = children

    context['toctree_elements'] = toctree_elements


def setup(app):
    app.connect('html-page-context', html_page_context)
