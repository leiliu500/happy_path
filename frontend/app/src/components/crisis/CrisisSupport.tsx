'use client'

import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ShieldExclamationIcon, XMarkIcon } from '@heroicons/react/24/outline'

export function CrisisSupport() {
  const [isVisible, setIsVisible] = useState(false)

  return (
    <>
      {/* Floating Crisis Button */}
      <motion.button
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ delay: 1, type: "spring", stiffness: 260, damping: 20 }}
        onClick={() => setIsVisible(true)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 bg-red-600 hover:bg-red-700 text-white rounded-full shadow-2xl flex items-center justify-center animate-pulse-soft"
        title="Crisis Support - Always Available"
      >
        <ShieldExclamationIcon className="w-7 h-7" />
      </motion.button>

      {/* Crisis Support Modal */}
      <AnimatePresence>
        {isVisible && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
            onClick={() => setIsVisible(false)}
          >
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
              className="bg-white rounded-2xl p-6 max-w-lg w-full shadow-2xl max-h-[90vh] overflow-y-auto"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
                    <ShieldExclamationIcon className="w-6 h-6 text-red-600" />
                  </div>
                  <div>
                    <h2 className="text-h2 font-bold text-neutral-900">
                      Crisis Support
                    </h2>
                    <p className="text-body-sm text-neutral-600">
                      Available 24/7 - You're not alone
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => setIsVisible(false)}
                  className="p-2 hover:bg-neutral-100 rounded-full transition-colors"
                >
                  <XMarkIcon className="w-5 h-5" />
                </button>
              </div>

              {/* Immediate Crisis Resources */}
              <div className="crisis-alert mb-6">
                <h3 className="font-semibold text-red-800 mb-3 flex items-center">
                  🚨 Immediate Emergency
                </h3>
                <p className="text-body-sm text-red-700 mb-4">
                  If you're in immediate danger, having thoughts of suicide, or in a mental health crisis:
                </p>
                <div className="space-y-3">
                  <a
                    href="tel:988"
                    className="block w-full text-center bg-red-600 hover:bg-red-700 text-white font-semibold py-4 px-4 rounded-xl transition-colors shadow-lg"
                  >
                    📞 Call 988 - Suicide & Crisis Lifeline
                    <div className="text-sm opacity-90 mt-1">Free, confidential, 24/7</div>
                  </a>
                  <a
                    href="sms:741741&body=HOME"
                    className="block w-full text-center bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-4 rounded-xl transition-colors shadow-lg"
                  >
                    💬 Text HOME to 741741
                    <div className="text-sm opacity-90 mt-1">Crisis Text Line</div>
                  </a>
                  <a
                    href="tel:911"
                    className="block w-full text-center bg-red-800 hover:bg-red-900 text-white font-semibold py-4 px-4 rounded-xl transition-colors shadow-lg"
                  >
                    🚨 Call 911
                    <div className="text-sm opacity-90 mt-1">Emergency Services</div>
                  </a>
                </div>
              </div>

              {/* Additional Support Resources */}
              <div className="space-y-4">
                <div className="bg-blue-50 rounded-xl p-4 border border-blue-200">
                  <h3 className="font-semibold text-blue-800 mb-3">
                    💙 Additional Support Lines
                  </h3>
                  <div className="space-y-2 text-body-sm text-blue-700">
                    <div className="flex justify-between">
                      <span>LGBTQ+ Crisis Support:</span>
                      <a href="tel:1-866-488-7386" className="font-medium underline">
                        1-866-488-7386
                      </a>
                    </div>
                    <div className="flex justify-between">
                      <span>Veterans Crisis Line:</span>
                      <a href="tel:1-800-273-8255" className="font-medium underline">
                        1-800-273-8255
                      </a>
                    </div>
                    <div className="flex justify-between">
                      <span>Teen Line:</span>
                      <a href="tel:1-800-852-8336" className="font-medium underline">
                        1-800-852-8336
                      </a>
                    </div>
                  </div>
                </div>

                <div className="bg-green-50 rounded-xl p-4 border border-green-200">
                  <h3 className="font-semibold text-green-800 mb-3">
                    🌐 Online Resources
                  </h3>
                  <div className="space-y-2 text-body-sm text-green-700">
                    <div>
                      <strong>Crisis Chat:</strong>{' '}
                      <a 
                        href="https://suicidepreventionlifeline.org/chat/" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="underline"
                      >
                        suicidepreventionlifeline.org/chat
                      </a>
                    </div>
                    <div>
                      <strong>Crisis Resources:</strong>{' '}
                      <a 
                        href="https://findtreatment.samhsa.gov/" 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="underline"
                      >
                        SAMHSA Treatment Locator
                      </a>
                    </div>
                  </div>
                </div>

                <div className="bg-purple-50 rounded-xl p-4 border border-purple-200">
                  <h3 className="font-semibold text-purple-800 mb-3">
                    🏥 Professional Help
                  </h3>
                  <p className="text-body-sm text-purple-700 mb-3">
                    Need ongoing support? We can help you find professional care:
                  </p>
                  <button className="w-full bg-purple-600 hover:bg-purple-700 text-white font-medium py-3 px-4 rounded-lg transition-colors">
                    Find Mental Health Professionals Near You
                  </button>
                </div>
              </div>

              {/* Safety Plan Reminder */}
              <div className="mt-6 bg-amber-50 rounded-xl p-4 border border-amber-200">
                <h3 className="font-semibold text-amber-800 mb-2">
                  📋 Create a Safety Plan
                </h3>
                <p className="text-body-sm text-amber-700 mb-3">
                  Having a safety plan can help during difficult moments. Would you like help creating one?
                </p>
                <button className="w-full bg-amber-600 hover:bg-amber-700 text-white font-medium py-2 px-4 rounded-lg transition-colors">
                  Start Safety Plan
                </button>
              </div>

              {/* Important Disclaimer */}
              <div className="mt-6 p-4 bg-neutral-50 rounded-xl border border-neutral-200">
                <p className="text-body-sm text-neutral-600">
                  <strong>Important:</strong> This platform provides wellness support and is NOT a licensed therapist 
                  or mental health professional. In crisis situations, always contact emergency services or the 
                  resources listed above.
                </p>
              </div>

              <button
                onClick={() => setIsVisible(false)}
                className="mt-6 btn-outline w-full py-3"
              >
                Close
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
