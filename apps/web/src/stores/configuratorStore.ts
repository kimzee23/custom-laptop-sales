import { create } from 'zustand'
import { 
  LaptopConfigurationState, 
  ConfigurationPriceBreakdown, 
  Product, 
  ArtworkConfiguration 
} from '@/types'
import { api } from '@/lib/api'

interface ConfiguratorStore {
  isOpen: boolean
  activeStep: number
  selectedProduct: Product | null
  config: LaptopConfigurationState
  breakdown: ConfigurationPriceBreakdown
  isCalculating: boolean

  // Actions
  openConfigurator: (product: Product) => void
  closeConfigurator: () => void
  setStep: (step: number) => void
  setColor: (colorId: string) => void
  setRam: (ramId: string) => void
  setStorage: (storageId: string) => void
  setGpu: (gpuId: string) => void
  setDisplay: (displayId: string) => void
  setKeyboard: (keyboardId: string) => void
  toggleAccessory: (accessoryId: string) => void
  setArtwork: (artwork: ArtworkConfiguration | undefined) => void
  calculatePrice: () => Promise<void>
  resetConfig: () => void
}

const DEFAULT_CONFIG: LaptopConfigurationState = {
  productId: '',
  productTitle: '',
  basePrice: 0,
  colorId: 'opt-color-arctic',
  ramId: 'opt-ram-16',
  storageId: 'opt-ssd-1tb',
  gpuId: 'opt-gpu-rtx4060',
  displayId: 'opt-disp-ips',
  keyboardId: 'opt-kb-backlit',
  accessoryIds: [],
  artwork: undefined,
}

const DEFAULT_BREAKDOWN: ConfigurationPriceBreakdown = {
  productId: '',
  productTitle: '',
  basePrice: 0,
  items: [],
  subtotal: 0,
  shipping: 0,
  discount: 0,
  total: 0,
  currency: 'NGN',
  currencySymbol: '₦',
}

export const useConfiguratorStore = create<ConfiguratorStore>((set, get) => ({
  isOpen: false,
  activeStep: 0,
  selectedProduct: null,
  config: DEFAULT_CONFIG,
  breakdown: DEFAULT_BREAKDOWN,
  isCalculating: false,

  openConfigurator: (product: Product) => {
    const initialConfig: LaptopConfigurationState = {
      productId: product.id,
      productTitle: product.title,
      basePrice: product.base_price,
      colorId: 'opt-color-arctic',
      ramId: 'opt-ram-16',
      storageId: 'opt-ssd-1tb',
      gpuId: 'opt-gpu-rtx4060',
      displayId: 'opt-disp-ips',
      keyboardId: 'opt-kb-backlit',
      accessoryIds: [],
      artwork: undefined,
    }
    set({
      isOpen: true,
      selectedProduct: product,
      config: initialConfig,
      activeStep: 0,
    })
    get().calculatePrice()
  },

  closeConfigurator: () => set({ isOpen: false }),
  setStep: (step: number) => set({ activeStep: step }),

  setColor: (colorId) => {
    set((state) => ({ config: { ...state.config, colorId } }))
    get().calculatePrice()
  },

  setRam: (ramId) => {
    set((state) => ({ config: { ...state.config, ramId } }))
    get().calculatePrice()
  },

  setStorage: (storageId) => {
    set((state) => ({ config: { ...state.config, storageId } }))
    get().calculatePrice()
  },

  setGpu: (gpuId) => {
    set((state) => ({ config: { ...state.config, gpuId } }))
    get().calculatePrice()
  },

  setDisplay: (displayId) => {
    set((state) => ({ config: { ...state.config, displayId } }))
    get().calculatePrice()
  },

  setKeyboard: (keyboardId) => {
    set((state) => ({ config: { ...state.config, keyboardId } }))
    get().calculatePrice()
  },

  toggleAccessory: (accessoryId) => {
    set((state) => {
      const exists = state.config.accessoryIds.includes(accessoryId)
      const accessoryIds = exists
        ? state.config.accessoryIds.filter((id) => id !== accessoryId)
        : [...state.config.accessoryIds, accessoryId]
      return { config: { ...state.config, accessoryIds } }
    })
    get().calculatePrice()
  },

  setArtwork: (artwork) => {
    set((state) => ({ config: { ...state.config, artwork } }))
    get().calculatePrice()
  },

  calculatePrice: async () => {
    const { config, selectedProduct } = get()
    if (!selectedProduct) return

    set({ isCalculating: true })

    try {
      const data = await api.calculatePrice({
        product_id: config.productId,
        color_id: config.colorId,
        ram_id: config.ramId,
        storage_id: config.storageId,
        gpu_id: config.gpuId,
        display_id: config.displayId,
        keyboard_id: config.keyboardId,
        accessory_ids: config.accessoryIds,
        artwork: config.artwork,
      })

      if (data) {
        set({ breakdown: data, isCalculating: false })
        return
      }
    } catch (e) {
      // Backend offline or during SSR build fallback
    }

    // Client-side fallback calculation
    let modifierTotal = 0
    const items = []

    // Color
    if (config.colorId === 'opt-color-arctic') {
      modifierTotal += 20000
      items.push({ name: 'Arctic Blue (Metallic)', category: 'Chassis Finish', modifier: 20000 })
    } else if (config.colorId === 'opt-color-cloud') {
      modifierTotal += 15000
      items.push({ name: 'Cloud White (Ceramic Finish)', category: 'Chassis Finish', modifier: 15000 })
    } else if (config.colorId === 'opt-color-midnight') {
      modifierTotal += 25000
      items.push({ name: 'Midnight Navy (Deep Matte)', category: 'Chassis Finish', modifier: 25000 })
    } else if (config.colorId === 'opt-color-crimson') {
      modifierTotal += 30000
      items.push({ name: 'Cyber Crimson (Stealth)', category: 'Chassis Finish', modifier: 30000 })
    }

    // RAM
    if (config.ramId === 'opt-ram-32') {
      modifierTotal += 90000
      items.push({ name: '32GB DDR5 5600MHz', category: 'RAM', modifier: 90000 })
    } else if (config.ramId === 'opt-ram-64') {
      modifierTotal += 210000
      items.push({ name: '64GB DDR5 6000MHz', category: 'RAM', modifier: 210000 })
    }

    // Storage
    if (config.storageId === 'opt-ssd-2tb') {
      modifierTotal += 130000
      items.push({ name: '2TB PCIe 4.0 NVMe SSD', category: 'Storage', modifier: 130000 })
    } else if (config.storageId === 'opt-ssd-4tb') {
      modifierTotal += 280000
      items.push({ name: '4TB Dual NVMe SSD', category: 'Storage', modifier: 280000 })
    }

    // GPU
    if (config.gpuId === 'opt-gpu-rtx4070') {
      modifierTotal += 320000
      items.push({ name: 'NVIDIA GeForce RTX 4070 8GB', category: 'GPU', modifier: 320000 })
    } else if (config.gpuId === 'opt-gpu-rtx4080') {
      modifierTotal += 680000
      items.push({ name: 'NVIDIA GeForce RTX 4080 12GB', category: 'GPU', modifier: 680000 })
    }

    // Display
    if (config.displayId === 'opt-disp-oled') {
      modifierTotal += 160000
      items.push({ name: '16" 3.2K OLED 120Hz 100% DCI-P3', category: 'Display', modifier: 160000 })
    }

    // Keyboard
    if (config.keyboardId === 'opt-kb-rgb') {
      modifierTotal += 45000
      items.push({ name: 'Per-Key RGB Mechanical Keyboard', category: 'Keyboard', modifier: 45000 })
    }

    // Artwork
    if (config.artwork && (config.artwork.image_url || config.artwork.custom_text)) {
      modifierTotal += 35000
      items.push({ name: 'Custom UV Artwork / Laser Engraving', category: 'Artwork', modifier: 35000 })
    }

    const subtotal = selectedProduct.base_price + modifierTotal
    set({
      breakdown: {
        productId: selectedProduct.id,
        productTitle: selectedProduct.title,
        basePrice: selectedProduct.base_price,
        items,
        subtotal,
        shipping: 0,
        discount: 0,
        total: subtotal,
        currency: 'NGN',
        currencySymbol: '₦',
      },
      isCalculating: false,
    })
  },

  resetConfig: () => set({ config: DEFAULT_CONFIG, breakdown: DEFAULT_BREAKDOWN, activeStep: 0 })
}))
