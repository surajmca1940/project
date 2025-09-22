// Service Worker for Booking System Performance Optimization
const CACHE_NAME = 'booking-system-v1.2';
const urlsToCache = [
    '/static/css/booking-enhanced.css',
    '/static/js/booking-optimized.js',
    '/static/css/style.css',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.7.2/font/bootstrap-icons.css',
    // Add other static assets
];

// Install event - cache resources
self.addEventListener('install', event => {
    console.log('Service Worker installing...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Caching booking system resources');
                return cache.addAll(urlsToCache);
            })
            .then(() => {
                console.log('Service Worker installed successfully');
                self.skipWaiting();
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker activating...');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('Service Worker activated');
            self.clients.claim();
        })
    );
});

// Fetch event - serve cached resources with network fallback
self.addEventListener('fetch', event => {
    // Only cache GET requests
    if (event.request.method !== 'GET') {
        return;
    }

    // Cache strategy: Cache First for static assets, Network First for API calls
    if (isStaticAsset(event.request.url)) {
        event.respondWith(cacheFirstStrategy(event.request));
    } else if (isAPICall(event.request.url)) {
        event.respondWith(networkFirstStrategy(event.request));
    } else {
        event.respondWith(networkFirstStrategy(event.request));
    }
});

function isStaticAsset(url) {
    return url.includes('/static/') || 
           url.includes('bootstrap-icons') ||
           url.includes('fonts.googleapis.com');
}

function isAPICall(url) {
    return url.includes('/api/') || 
           url.includes('/booking/') ||
           url.includes('get_availability');
}

// Cache First Strategy - for static assets
function cacheFirstStrategy(request) {
    return caches.match(request)
        .then(response => {
            if (response) {
                return response; // Return cached version
            }
            
            // If not in cache, fetch from network and cache it
            return fetch(request).then(response => {
                if (!response || response.status !== 200 || response.type !== 'basic') {
                    return response;
                }
                
                const responseToCache = response.clone();
                caches.open(CACHE_NAME)
                    .then(cache => {
                        cache.put(request, responseToCache);
                    });
                
                return response;
            });
        })
        .catch(() => {
            // Offline fallback for critical resources
            if (request.url.includes('.css')) {
                return new Response('/* Offline fallback styles */', {
                    headers: { 'Content-Type': 'text/css' }
                });
            }
            if (request.url.includes('.js')) {
                return new Response('console.log("Offline mode");', {
                    headers: { 'Content-Type': 'application/javascript' }
                });
            }
        });
}

// Network First Strategy - for API calls and dynamic content
function networkFirstStrategy(request) {
    return fetch(request)
        .then(response => {
            // Clone the response before using it
            const responseToCache = response.clone();
            
            // Cache successful responses
            if (response.status === 200) {
                caches.open(CACHE_NAME)
                    .then(cache => {
                        cache.put(request, responseToCache);
                    });
            }
            
            return response;
        })
        .catch(() => {
            // Fallback to cache if network fails
            return caches.match(request)
                .then(response => {
                    if (response) {
                        return response;
                    }
                    
                    // Ultimate fallback for booking pages
                    if (request.url.includes('/booking/')) {
                        return new Response(
                            JSON.stringify({ 
                                error: 'Offline', 
                                message: 'Please check your internet connection' 
                            }),
                            { 
                                headers: { 'Content-Type': 'application/json' },
                                status: 503
                            }
                        );
                    }
                    
                    throw new Error('Network error and no cache available');
                });
        });
}

// Background sync for offline bookings (if needed)
self.addEventListener('sync', event => {
    if (event.tag === 'background-sync-booking') {
        console.log('Background sync triggered for booking');
        event.waitUntil(syncBookingData());
    }
});

function syncBookingData() {
    // Implementation for syncing offline booking data
    return Promise.resolve();
}

// Push notifications (if needed for booking reminders)
self.addEventListener('push', event => {
    if (event.data) {
        const data = event.data.json();
        const options = {
            body: data.body,
            icon: '/static/icons/booking-icon.png',
            badge: '/static/icons/badge.png',
            tag: 'booking-reminder',
            requireInteraction: false,
            actions: [
                {
                    action: 'view',
                    title: 'View Appointment',
                    icon: '/static/icons/view.png'
                },
                {
                    action: 'dismiss',
                    title: 'Dismiss',
                    icon: '/static/icons/dismiss.png'
                }
            ]
        };
        
        event.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

// Handle notification clicks
self.addEventListener('notificationclick', event => {
    event.notification.close();
    
    if (event.action === 'view') {
        event.waitUntil(
            clients.openWindow('/booking/my-appointments/')
        );
    }
    // 'dismiss' action doesn't need handling as notification is already closed
});