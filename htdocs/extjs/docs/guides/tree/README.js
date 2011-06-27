Ext.data.JsonP.tree({
  "guide": "<h1>Tree</h1>\n\n<hr />\n\n<p>Ext JS 4.0 introduces a solid foundation for one of our most versatile components - Tree.  Tree and grid now both extend from the same base class. All of the benefits of grid - features, extensions, and plugins can now be used on trees. Things like columns, column resizing, dragging and dropping, renderers, sorting and filtering can now be expected to work similarly for both components. Additionally, we are planning on implementing new features to do things like paging and buffered rendering for very large trees.</p>\n\n<p>Lets start by creating a very simple Tree.</p>\n\n<pre><code>var tree = Ext.create('Ext.tree.Panel', {\n    title: 'Simple Tree',\n    root: {\n        text: 'Root',\n        expanded: true,\n        children: [{\n            text: 'Child 1',\n            leaf: true\n        }, {\n            text: 'Child 2',\n            leaf: true\n        }]\n    }\n});\n</code></pre>\n\n<p>We have defined a root node for our tree and told it to be expanded. We also defined two children inline, both of which we said are leaf nodes. Setting the <strong>leaf</strong> config to true indicates that the node won't be able to contain child nodes. The text property, like the name suggests, is used as the node's text label. The tree that this code produces looks like the following.</p>\n\n<p><img src=\"guides/tree/simple-tree.png\" alt=\"Simple Tree\" /></p>\n\n<p>The base class that Tree extends from, <a href=\"#/api/Ext.panel.Table\" rel=\"Ext.panel.Table\" class=\"docClass\">Ext.panel.Table</a>, is responsible for several things.</p>\n\n<ul>\n<li>Setting up and managing a (data)view</li>\n<li>Binding to a store</li>\n<li>Creating a header container</li>\n<li>Creating a selection model</li>\n</ul>\n\n\n<p>In the case of <a href=\"#/api/Ext.tree.Panel\" rel=\"Ext.tree.Panel\" class=\"docClass\">Ext.tree.Panel</a>, the store has to be an instance of <a href=\"#/api/Ext.data.TreeStore\" rel=\"Ext.data.TreeStore\" class=\"docClass\">Ext.data.TreeStore</a>, the view will be an instance of <a href=\"#/api/Ext.tree.View\" rel=\"Ext.tree.View\" class=\"docClass\">Ext.tree.View</a> and the selection model by default is an instance of Ext.selection.TreeModel.</p>\n\n<p>In order to make setting up a tree as easy as possible, we make some assumptions internally. Sometimes you want your tree to behave or look differently. Fortunately, there are many configurations at our disposal to do so. We will start with visual configurations, and then dive into the data structures behind our tree.</p>\n\n<h2>Visually changing your tree</h2>\n\n<p>Let's try something simple. When you set the <strong>useArrows</strong> configuration to true, we hide the lines and use arrows as expand and collapse icons.</p>\n\n<p><img src=\"guides/tree/arrows.png\" alt=\"Arrows\" /></p>\n\n<p>Sometimes you don't want the root node to be visible. Setting the <strong>rootVisible</strong> property to false visually removes the root node. By doing this, your root node will automatically be expanded. The following image shows the same tree with <strong>rootVisible</strong> set to false. We have also set <strong>lines</strong> false.</p>\n\n<p><img src=\"guides/tree/root-lines.png\" alt=\"Root not visible and no lines\" /></p>\n\n<p>TODO: icon and iconCls</p>\n\n<h2>Multiple columns</h2>\n\n<p>Since our tree now extends a grid, adding more columns is very easy to do.</p>\n\n<pre><code>var tree = Ext.create('Ext.tree.Panel', {\n    title: 'TreeGrid',\n    fields: ['name', 'description'],\n    columns: [{\n        xtype: 'treecolumn',\n        text: 'Name',\n        dataIndex: 'name',\n        width: 150,\n        sortable: true\n    }, {\n        text: 'Description',\n        dataIndex: 'description',\n        flex: 1,\n        sortable: true\n    }],\n    root: {\n        name: 'Root',\n        description: 'Root description',\n        expanded: true,\n        children: [{\n            name: 'Child 1',\n            description: 'Description 1',\n            leaf: true\n        }, {\n            name: 'Child 2',\n            description: 'Description 2',\n            leaf: true\n        }]\n    }\n});\n</code></pre>\n\n<p>We have defined the columns configuration. The available configurations are exactly the same as those available for grid columns. You can use any type of column you would use in a grid. The only requirement when using multiple columns in a Tree is that you must supply at least one column with an xtype of <strong>treecolumn</strong>. This column decorates the column's renderer to visualize things like depth, lines and the expand and collapse icons. You usually want to create only one column of this type in your tree.</p>\n\n<p>We also specified the <strong>fields</strong> configuration, which will be passed on to the internally created store. We will get into this in more detail later in the guide, but for now just notice how the <strong>dataIndex</strong> configurations on the columns map to the fields we specified - name and description.</p>\n\n<p><img src=\"guides/tree/treegrid.png\" alt=\"Tree and a Grid\" /></p>\n\n<p>It is also worth noting that when you don't specify columns, the tree will automatically create one single <strong>treecolumn</strong> for you with a <strong>dataIndex</strong> set to 'text'. It also hides the headers on the tree. If you want to show this header when using only a single column, you can set the <strong>hideHeaders</strong> configuration to 'false'.</p>\n\n<h2>Events</h2>\n\n<p>Info about tree events here</p>\n\n<h2>Adding nodes to the tree</h2>\n\n<p>So far we haven't specified a store in any of our code. Since we haven't done so the tree will create a TreeStore for you and pass the root configuration to this store. This internally created TreeStore will get a memory proxy by default. This means that you can't load nodes from the server asynchronously. Instead you are expected to append all the nodes to your tree programmatically. We will look at how to do this in a little bit.</p>\n\n<p>Note that when you create a tree this way, you don't necessarily have to specify a root node right away. The following will achieve the exact same result except now we dynamically set the root node after the tree has been created.</p>\n\n<pre><code>var tree = Ext.create('Ext.tree.Panel');\ntree.setRootNode({\n    text: 'Root',\n    expanded: true,\n    children: [{\n        text: 'Child 1',\n        leaf: true\n    }, {\n        text: 'Child 2',\n        leaf: true\n    }]\n});\n</code></pre>\n\n<p>Although this is useful for very small trees with only a few static nodes, usually your tree will contain many more nodes. So let's take a look at how we can programmatically add new nodes to the tree.</p>\n\n<pre><code>var root = tree.getRootNode();\n\nvar parent = root.appendChild({\n    text: 'Parent 1'\n});\n\nparent.appendChild({\n    text: 'Child 3',\n    leaf: true\n});\n\nparent.expand();\n</code></pre>\n\n<p>When adding new nodes to the tree, you always need to get a reference to the parent you want to append the new node to. In this case we got a reference to the root node. You can call <em>appendChild</em> on any node in the tree that is not a leaf. It accepts a node instance or an object containing data that will be used to create a new node. The method always returns a fully instantiated node. In this example we programmatically call the <em>expand</em> method to expand our newly created parent.</p>\n\n<p><img src=\"guides/tree/append-children.png\" alt=\"Appending to the tree\" /></p>\n\n<p>We could have also just set the <strong>expanded</strong> configuration when defining the parent. Also useful is the ability to define children inline when creating the new parent nodes. The following code gives us the same result.</p>\n\n<pre><code>var parent = root.appendChild({\n    text: 'Parent 1',\n    expanded: true,\n    children: [{\n        text: 'Child 3',\n        leaf: true\n    }]\n});\n</code></pre>\n\n<p>Sometimes you will want to insert a node into a specific location in the tree instead of appending it. Besides the <em>appendChild</em> method, we also provide <em>insertBefore</em> and <em>insertChild</em> methods.</p>\n\n<pre><code>var child = parent.insertChild(0, {\n    text: 'Child 2.5',\n    leaf: true\n});\n\nparent.insertBefore({\n    text: 'Child 2.75',\n    leaf: true\n}, child.nextSibling);\n</code></pre>\n\n<p>As you can see the <em>insertChild</em> method expects an index at which the child will be inserted. The <em>insertBefore</em> method expects a reference node. Your new node will be inserted before that node.</p>\n\n<p><img src=\"guides/tree/insert-children.png\" alt=\"Inserting children into the tree\" /></p>\n\n<p>One other thing to note is the <strong>nextSibling</strong> property we used. There are several more properties on nodes that we can use to reference other nodes.</p>\n\n<ul>\n<li>nextSibling</li>\n<li>previousSibling</li>\n<li>parentNode</li>\n<li>lastChild</li>\n<li>firstChild</li>\n<li>childNodes</li>\n</ul>\n\n\n<h2>The Node Interface</h2>\n\n<p>So far we have come across several methods and properties on nodes. But what are nodes exactly? As we have mentioned before, the tree Panel is bound to a TreeStore. A store in <a href=\"#/api/Ext\" rel=\"Ext\" class=\"docClass\">Ext</a> JS manages a collection of model instances. We created a NodeInterface that can be used to decorate any model with fields, methods and properties required to have to model be used in a tree. When we refer to a node, we essentially are referring to a model instance that is decorated with the NodeInterface. The following screenshot shows you by logging a node in the developer tools.</p>\n\n<p><img src=\"guides/tree/nodeinterface.png\" alt=\"A model instance decorated with the NodeInterface\" /></p>\n\n<p>In order to see the full set of fields, methods and properties available on nodes, you can check out the API documentation for the NodeInterface class.</p>\n\n<ul>\n<li>list these fields and explain briefly what each one does</li>\n</ul>\n\n\n<h2>The tree's Store</h2>\n\n<ul>\n<li>introduction to specifying your own store</li>\n<li>define your own model with a proxy to asynchronously retrieve nodes from the server</li>\n<li>show the same model instances in tree and grid at the same time</li>\n</ul>\n\n"
});