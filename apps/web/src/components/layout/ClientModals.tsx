'use client'

import { CartDrawer } from '@/components/cart/CartDrawer'
import { ConfiguratorModal } from '@/components/configurator/ConfiguratorModal'
import { CheckoutModal } from '@/components/checkout/CheckoutModal'
import { WishlistDrawer } from '@/components/wishlist/WishlistDrawer'
import { OrderTrackingModal } from '@/components/orders/OrderTrackingModal'
import { useCartStore } from '@/stores/cartStore'
import { useOrderTrackingStore } from '@/stores/orderTrackingStore'

export const ClientModals: React.FC = () => {
  const { isCheckoutOpen, setIsCheckoutOpen } = useCartStore()
  const { isOpen: isTrackingOpen, orderNumber: trackingOrderNumber, closeTracking } = useOrderTrackingStore()

  return (
    <>
      <CartDrawer />
      <ConfiguratorModal />
      <WishlistDrawer />
      <CheckoutModal 
        isOpen={isCheckoutOpen} 
        onClose={() => setIsCheckoutOpen(false)} 
      />
      <OrderTrackingModal
        isOpen={isTrackingOpen}
        initialOrderNumber={trackingOrderNumber}
        onClose={closeTracking}
      />
    </>
  )
}
