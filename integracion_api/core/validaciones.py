


def comprobar_minimo(self):
        month = self.kwargs.get('month')
        if not 1 <= int(month) <= 12:
            raise Http404("El mes proporcionado no es válido.")
        
        first_day_of_month = timezone.now().replace(month=int(month), day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_of_month = (first_day_of_month + timedelta(days=31)).replace(day=1) - timedelta(days=1)+

        return Transaccion.objects.filter(Q(pago__estado_pago__id_estado_pago=0) & Q(pedido__fecha__gte=first_day_of_month) & Q(pedido__fecha__lte=last_day_of_month))