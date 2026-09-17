import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        background: '#F6F9FF',
        navy: {
          DEFAULT: '#0B1F3A',
          deep: '#061325',
          light: '#132B4F',
        },
        primary: {
          DEFAULT: '#1769FF',
          hover: '#0E55DB',
          light: '#EAF2FF',
          soft: '#F0F5FF',
          sky: '#4DA3FF',
        },
        accent: {
          DEFAULT: '#4DA3FF',
          soft: '#EAF2FF',
        },
        foreground: '#10213A',
        muted: {
          DEFAULT: '#60708A',
          light: '#8FA0B8',
          bg: '#F0F4FA',
        },
        border: {
          DEFAULT: '#DCE6F5',
          dark: '#B9CEEB',
        },
        success: {
          DEFAULT: '#16A36A',
          light: '#E8F8F0',
        },
        error: {
          DEFAULT: '#D92D20',
          light: '#FDECEB',
        },
        discount: {
          DEFAULT: '#E5484D',
          light: '#FDE8E8',
        },
        warning: {
          DEFAULT: '#F59E0B',
          light: '#FEF3C7',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        display: ['Space Grotesk', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        'card': '0 2px 12px -2px rgba(11, 31, 58, 0.06), 0 1px 3px 0 rgba(11, 31, 58, 0.04)',
        'card-hover': '0 12px 30px -4px rgba(23, 105, 255, 0.12), 0 4px 12px -2px rgba(11, 31, 58, 0.06)',
        'dropdown': '0 10px 30px -5px rgba(11, 31, 58, 0.12), 0 4px 10px -2px rgba(11, 31, 58, 0.04)',
        'glow': '0 0 20px rgba(23, 105, 255, 0.35)',
      },
      borderRadius: {
        'card': '14px',
        'button': '10px',
      },
      animation: {
        'pulse-subtle': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 4s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-6px)' },
        }
      }
    },
  },
  plugins: [],
}
export default config
