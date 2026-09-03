const SOURCE = 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/orientation-review/gv-triangle-consensus-sandbox-0006.html';
const OLD_WORKER = 'https://gv-cloudflare-auto-astrometry-curator-0015.gear66me.workers.dev';

function corsHeaders(extra = {}) {
  return {
    'access-control-allow-origin': '*',
    'access-control-allow-methods': 'GET,HEAD,OPTIONS',
    'access-control-allow-headers': '*',
    ...extra
  };
}

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders() });
    }

    if (url.pathname === '/api/image') {
      const target = url.searchParams.get('url');
      if (!target || !/^https?:\/\//i.test(target)) {
        return new Response('Missing or invalid image url', {
          status: 400,
          headers: corsHeaders({ 'content-type': 'text/plain; charset=utf-8' })
        });
      }

      try {
        const upstream = await fetch(target, {
          redirect: 'follow',
          headers: {
            'User-Agent': 'Galaxy-Viewer-Triangle-Consensus-0006',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
          }
        });

        if (!upstream.ok) {
          return new Response('Image upstream HTTP ' + upstream.status, {
            status: 502,
            headers: corsHeaders({ 'content-type': 'text/plain; charset=utf-8' })
          });
        }

        const headers = corsHeaders({
          'content-type': upstream.headers.get('content-type') || 'application/octet-stream',
          'cache-control': 'public, max-age=3600',
          'x-gv-image-proxy': 'triangle-consensus-0006'
        });

        return new Response(upstream.body, { status: 200, headers });
      } catch (err) {
        return new Response('Image proxy fetch failed: ' + String(err?.message || err), {
          status: 502,
          headers: corsHeaders({ 'content-type': 'text/plain; charset=utf-8' })
        });
      }
    }

    if (url.pathname !== '/' && url.pathname !== '/index.html') {
      return new Response('Not Found', { status: 404 });
    }

    const upstream = await fetch(SOURCE, {
      cf: { cacheTtl: 60, cacheEverything: true },
      headers: { 'User-Agent': 'Galaxy-Viewer-Triangle-Consensus-0006' }
    });

    if (!upstream.ok) {
      return new Response('Triangle Consensus Sandbox source unavailable: HTTP ' + upstream.status, {
        status: 502,
        headers: { 'content-type': 'text/plain; charset=utf-8' }
      });
    }

    let html = await upstream.text();
    const origin = url.origin;
    html = html.split(OLD_WORKER).join(origin);

    return new Response(html, {
      status: 200,
      headers: {
        'content-type': 'text/html; charset=utf-8',
        'cache-control': 'no-store, max-age=0',
        'x-gv-sandbox': 'triangle-consensus-0006',
        'x-gv-image-proxy': 'same-origin'
      }
    });
  }
};
