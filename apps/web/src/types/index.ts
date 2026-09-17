export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  image_url?: string;
  icon?: string;
  display_order?: number;
  product_count?: number;
}

export interface Brand {
  id: string;
  name: string;
  slug: string;
  logo_url?: string;
}

export interface Product {
  id: string;
  title: string;
  slug: string;
  description?: string;
  short_description?: string;
  category_id?: string;
  brand_id?: string;
  category?: Category;
  brand?: Brand;
  base_price: number;
  original_price?: number;
  discount_percentage?: number;
  is_featured: boolean;
  is_flash_deal: boolean;
  is_best_seller: boolean;
  is_customizable: boolean;
  stock: number;
  rating: number;
  review_count: number;
  image_url: string;
  gallery_images: string[];
  specs: {
    processor?: string;
    ram?: string;
    storage?: string;
    gpu?: string;
    display?: string;
    battery?: string;
    weight?: string;
    ports?: string;
    material?: string;
    [key: string]: any;
  };
  model_3d_url?: string;
}

export interface ConfigurationOption {
  id: string;
  code: string;
  name: string;
  price_modifier: number;
  stock?: number;
  is_active?: boolean;
  display_order: number;
  metadata_json?: {
    hex?: string;
    speed?: string;
    badge?: string;
    default?: boolean;
    recommended?: boolean;
    has_uploader?: boolean;
    [key: string]: any;
  };
}

export interface ConfigurationCategory {
  id: string;
  code: 'color' | 'ram' | 'storage' | 'gpu' | 'display' | 'keyboard' | 'artwork' | 'accessories' | string;
  name: string;
  display_order: number;
  is_required: boolean;
  options: ConfigurationOption[];
}

export interface ArtworkConfiguration {
  image_url?: string;
  position_x: number;
  position_y: number;
  scale: number;
  rotation: number;
  custom_text?: string;
}

export interface LaptopConfigurationState {
  productId: string;
  productTitle: string;
  basePrice: number;
  colorId: string;
  ramId: string;
  storageId: string;
  cpuId?: string;
  gpuId?: string;
  displayId?: string;
  keyboardId?: string;
  accessoryIds: string[];
  artwork?: ArtworkConfiguration;
}

export interface PriceBreakdownItem {
  name: string;
  category: string;
  modifier: number;
}

export interface ConfigurationPriceBreakdown {
  productId: string;
  productTitle: string;
  basePrice: number;
  items: PriceBreakdownItem[];
  subtotal: number;
  shipping: number;
  discount: number;
  total: number;
  currency: string;
  currencySymbol: string;
}

export interface CartItem {
  id: string;
  productId: string;
  productTitle: string;
  imageUrl: string;
  quantity: number;
  unitPrice: number;
  totalPrice: number;
  configuration?: Partial<LaptopConfigurationState>;
  configurationSummary?: {
    color?: string;
    ram?: string;
    storage?: string;
    gpu?: string;
    display?: string;
    keyboard?: string;
    hasArtwork?: boolean;
  };
}
