// Service Worker for FTC Progressive Web App
const CACHE_NAME = 'ftc-pwa-v1.0.0';
const urlsToCache = [
  '/',
  '/assets/css/mobile-responsive.css',
  '/assets/css/style.css',
  '/assets/js/main.js',
  '/assets/img/logo.png',
  '/products',
  '/users',
  '/offline.html'
];

// Install Service Worker
self.addEventListener('install', event => {
  console.log('[SW] Installing Service Worker...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('[SW] Caching App Shell');
        return cache.addAll(urlsToCache);
      })
      .catch(err => console.log('[SW] Cache Error:', err))
  );
});

// Activate Service Worker
self.addEventListener('activate', event => {
  console.log('[SW] Activating Service Worker...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch Strategy: Network First with Cache Fallback
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    fetch(event.request)
      .then(response => {
        // Check if we received a valid response
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }

        // Clone the response for caching
        const responseToCache = response.clone();
        
        caches.open(CACHE_NAME)
          .then(cache => {
            cache.put(event.request, responseToCache);
          });

        return response;
      })
      .catch(() => {
        // Network failed, try cache
        return caches.match(event.request)
          .then(response => {
            if (response) {
              return response;
            }
            
            // Show offline page for navigation requests
            if (event.request.mode === 'navigate') {
              return caches.match('/offline.html');
            }
          });
      })
  );
});

// Background Sync for Order Submissions
self.addEventListener('sync', event => {
  if (event.tag === 'order-submission') {
    event.waitUntil(
      syncOrderSubmissions()
    );
  }
});

// Push Notifications
self.addEventListener('push', event => {
  const options = {
    body: event.data ? event.data.text() : 'New update from FTC!',
    icon: '/assets/img/icon-192x192.png',
    badge: '/assets/img/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    },
    actions: [
      {
        action: 'explore',
        title: 'View Details',
        icon: '/assets/img/checkmark.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/assets/img/xmark.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('FTC Marketplace', options)
  );
});

// Notification Click Handling
self.addEventListener('notificationclick', event => {
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/products')
    );
  } else if (event.action === 'close') {
    // Just close the notification
  } else {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Helper function for background sync
async function syncOrderSubmissions() {
  try {
    const cache = await caches.open(CACHE_NAME + '-data');
    const requests = await cache.keys();
    
    for (const request of requests) {
      if (request.url.includes('/orders/submit')) {
        try {
          await fetch(request);
          await cache.delete(request);
        } catch (error) {
          console.log('[SW] Failed to sync order:', error);
        }
      }
    }
  } catch (error) {
    console.log('[SW] Sync failed:', error);
  }
}