define([
    'plugins/netmap-extras',
    'libs-amd/text!netmap/templates/modal/save_new_map.html',
    'libs/handlebars',
    'libs/jquery',
    'libs/underscore',
    'libs/backbone',
    'libs/jquery-ui-1.8.21.custom.min'
], function (NetmapHelpers, template) {

    var modalSaveNew = Backbone.View.extend({
        events: {
            "click #modal_save_view_button": "save_view",
            "submit": function () { return false; }
        },
        initialize: function () {
            this.template_post = Handlebars.compile(template);

            if (!this.options.graph || !this.options.model) {
                alert("Missing graph data or view properties, cannot save!");
                this.close();
            } else {

                this.el = $(this.template_post({'model': this.model.toJSON(), 'is_new': this.model.isNew()})).dialog({autoOpen: false});
                this.$el = $(this.el);

                this.model.bind("change", this.render, this);
                this.model.bind("destroy", this.close, this);
            }
        },
        render: function () {
            this.el.dialog('open');
            return this;
        },
        get_fixed_nodes: function () {
            var fixed_nodes = _.filter(this.options.graph.get('nodes'), function (node) {
                return node.fixed === true && node.data.category !== 'elink';
            });
            return fixed_nodes;
        },
        save_view: function () {
            var self = this;

            this.model.set({
                title: self.$('#new_view_title').val().trim(),
                description: self.$('#new_view_description').val().trim(),
                is_public: self.$('#new_view_is_public').prop('checked'),
                nodes: self.get_fixed_nodes(),
                topology: self.model.get('topology'),
                categories: self.model.get('categories'),
                zoom: self.model.get('zoom'),
                display_orphans: !self.model.get('display_orphans')
            });

            this.model.save(this.model.attributes, {
                wait: true,
                error: function () { alert("Error while saving view, try again"); },
                success: function (model, response) {
                    model.set({'viewid': response});
                    Backbone.View.navigate("view/{0}".format(response));
                }
            });
            this.close();
        },
        close: function () {
            $('#modal_new_view').dialog('destroy').remove();
            $(this.el).unbind();
            $(this.el).remove();
        }
    });
    return modalSaveNew;
});
