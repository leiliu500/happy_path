'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Bars3Icon, 
  XMarkIcon, 
  BellIcon, 
  UserCircleIcon,
  ShieldExclamationIcon 
} from '@heroicons/react/24/outline'

interface HeaderProps {
  showNavigation?: boolean
}

export function Header({ showNavigation = false }: HeaderProps) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [showCrisisMenu, setShowCrisisMenu] = useState(false)

  const navigationItems = [
    { label: 'Dashboard', href: '/dashboard' },
    { label: 'Wellness', href: '/wellness' },
    { label: 'Community', href: '/community' },
    { label: 'Resources', href: '/resources' }
  ]

  return (
    <>
      <motion.header
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-neutral-200"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="flex items-center space-x-3"
            >
              <div className="w-10 h-10 rounded-full bg-gradient-to-br from-secondary-500 to-accent-500 flex items-center justify-center">
                <span className="text-white font-bold text-lg">🌱</span>
              </div>
              <div>
                <h1 className="text-h3 font-bold text-neutral-900">Happy Path</h1>
                <p className="text-caption text-neutral-500 -mt-1">Mental Wellness</p>
              </div>
            </motion.div>

            {/* Desktop Navigation */}
            {showNavigation && (
              <nav className="hidden md:flex items-center space-x-8">
                {navigationItems.map((item) => (
                  <a
                    key={item.label}
                    href={item.href}
                    className="text-body text-neutral-600 hover:text-secondary-600 transition-colors duration-200 font-medium"
                  >
                    {item.label}
                  </a>
                ))}
              </nav>
            )}

            {/* Right Side Actions */}
            <div className="flex items-center space-x-4">
              {/* Crisis Support Button */}
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setShowCrisisMenu(true)}
                className="crisis-button px-4 py-2 text-body-sm"
              >
                <ShieldExclamationIcon className="w-5 h-5 mr-2 inline" />
                Crisis Support
              </motion.button>

              {showNavigation && (
                <>
                  {/* Notifications */}
                  <button className="relative p-2 text-neutral-600 hover:text-secondary-600 transition-colors">
                    <BellIcon className="w-6 h-6" />
                    <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                      3
                    </span>
                  </button>

                  {/* Profile */}
                  <button className="p-2 text-neutral-600 hover:text-secondary-600 transition-colors">
                    <UserCircleIcon className="w-6 h-6" />
                  </button>
                </>
              )}

              {/* Mobile Menu Button */}
              {showNavigation && (
                <button
                  onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                  className="md:hidden p-2 text-neutral-600 hover:text-secondary-600 transition-colors"
                >
                  {isMobileMenuOpen ? (
                    <XMarkIcon className="w-6 h-6" />
                  ) : (
                    <Bars3Icon className="w-6 h-6" />
                  )}
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Mobile Navigation */}
        <AnimatePresence>
          {isMobileMenuOpen && showNavigation && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="md:hidden bg-white border-t border-neutral-200"
            >
              <div className="px-4 py-4 space-y-4">
                {navigationItems.map((item) => (
                  <a
                    key={item.label}
                    href={item.href}
                    className="block text-body text-neutral-600 hover:text-secondary-600 transition-colors duration-200 font-medium py-2"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    {item.label}
                  </a>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.header>

      {/* Crisis Support Modal */}
      <CrisisModal 
        isOpen={showCrisisMenu} 
        onClose={() => setShowCrisisMenu(false)} 
      />
    </>
  )
}

// Crisis Support Modal Component
function CrisisModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  if (!isOpen) return null

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
      onClick={onClose}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        onClick={(e) => e.stopPropagation()}
        className="bg-white rounded-2xl p-8 max-w-md w-full shadow-2xl"
      >
        <div className="text-center">
          <div className="w-16 h-16 mx-auto mb-6 rounded-full bg-red-100 flex items-center justify-center">
            <ShieldExclamationIcon className="w-8 h-8 text-red-600" />
          </div>
          
          <h2 className="text-h2 font-bold text-neutral-900 mb-4">
            Crisis Support Resources
          </h2>
          
          <div className="space-y-4 text-left">
            <div className="crisis-alert">
              <h3 className="font-semibold text-red-800 mb-2">
                Immediate Emergency
              </h3>
              <p className="text-body-sm text-red-700 mb-3">
                If you're in immediate danger or having thoughts of suicide:
              </p>
              <div className="space-y-2">
                <a
                  href="tel:988"
                  className="block w-full text-center bg-red-600 hover:bg-red-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
                >
                  📞 Call 988 (Suicide & Crisis Lifeline)
                </a>
                <a
                  href="tel:911"
                  className="block w-full text-center bg-red-800 hover:bg-red-900 text-white font-semibold py-3 px-4 rounded-lg transition-colors"
                >
                  🚨 Call 911 (Emergency Services)
                </a>
              </div>
            </div>

            <div className="bg-blue-50 rounded-lg p-4 border border-blue-200">
              <h3 className="font-semibold text-blue-800 mb-2">
                24/7 Support Options
              </h3>
              <div className="space-y-2 text-body-sm">
                <div>
                  <strong>Crisis Text Line:</strong> Text HOME to 741741
                </div>
                <div>
                  <strong>Online Chat:</strong> Available 24/7 at suicidepreventionlifeline.org
                </div>
                <div>
                  <strong>LGBTQ+ Support:</strong> Call 1-866-488-7386
                </div>
              </div>
            </div>
          </div>

          <button
            onClick={onClose}
            className="mt-6 btn-outline w-full"
          >
            Close
          </button>
        </div>
      </motion.div>
    </motion.div>
  )
}
