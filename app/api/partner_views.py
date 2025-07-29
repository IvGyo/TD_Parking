class PartnerStatsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_parking_lots = ParkingLot.objects.filter(owner=request.user)
        
        stats = {
            'total_revenue': 0,
            'monthly_vehicles': 0,
            'occupancy_rate': 0,
            'parking_lots': []
        }
        
        for lot in user_parking_lots:
            lot_stats = self.calculate_lot_stats(lot)
            stats['parking_lots'].append(lot_stats)
            stats['total_revenue'] += lot_stats['revenue']
        
        return Response(stats)
