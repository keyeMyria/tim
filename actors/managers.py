class ClientsManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(type='client')

class ReportersManager(models.Manager):
    def get_queryset(self):
        return super(Reporters, self).get_queryset().filter(type='reporter')
