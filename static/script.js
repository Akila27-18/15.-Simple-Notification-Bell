document.addEventListener('DOMContentLoaded', () => {
    const badge = document.getElementById('badgeCount');
    const list = document.getElementById('notificationList');
  
    async function fetchNotifications() {
      try {
        const res = await fetch('/api/notifications');
        const data = await res.json();
  
        // Update badge count
        badge.textContent = data.unread_count;
        badge.style.display = data.unread_count > 0 ? 'inline-block' : 'none';
  
        // Fill modal content
        list.innerHTML = '';
        data.notifications.forEach(n => {
          const item = document.createElement('div');
          item.className = `alert ${n.is_read ? 'alert-secondary' : 'alert-primary'} mb-2`;
          item.innerHTML = `<strong>${n.title}</strong><br><small>${n.message}</small>`;
          list.appendChild(item);
        });
      } catch (err) {
        console.error('Error fetching notifications:', err);
      }
    }
  
    // Initial fetch
    fetchNotifications();
  
    // Every 10 seconds
    setInterval(fetchNotifications, 10000);
  
    // Fetch again when modal is opened
    document.getElementById('notificationBtn').addEventListener('click', fetchNotifications);
  });
  