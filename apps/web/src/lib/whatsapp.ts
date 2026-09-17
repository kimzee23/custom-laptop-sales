export const WHATSAPP_PHONE_DISPLAY = '0708 425 6460';
export const WHATSAPP_PHONE_INTL = '2347084256460';

export function getWhatsAppQuoteUrl(options?: {
  productTitle?: string;
  price?: number;
  specsSummary?: string;
  customNotes?: string;
}): string {
  let message = `Hello RealTech Customer Care! 👋\nI would like to get a quote & discuss a direct deal for custom laptops.`;

  if (options?.productTitle) {
    message += `\n\n📌 Model: ${options.productTitle}`;
  }

  if (options?.specsSummary) {
    message += `\n⚙️ Specifications: ${options.specsSummary}`;
  }

  if (options?.price) {
    message += `\n💰 Estimated Price: ₦${options.price.toLocaleString()}`;
  }

  if (options?.customNotes) {
    message += `\n📝 Note: ${options.customNotes}`;
  }

  message += `\n\nPlease let me know availability, best direct pricing, and delivery timeline. Thank you!`;

  return `https://wa.me/${WHATSAPP_PHONE_INTL}?text=${encodeURIComponent(message)}`;
}
