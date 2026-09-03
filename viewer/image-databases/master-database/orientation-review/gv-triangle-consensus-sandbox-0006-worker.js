const SOURCE = 'https://raw.githubusercontent.com/gear66me-ui/Galaxy_Viewer/beta/viewer/image-databases/master-database/orientation-review/gv-triangle-consensus-sandbox-0006.html';

export default {
  async fetch(request) {
    const url = new URL(request.url);
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

    const html = await upstream.text();
    return new Response(html, {
      status: 200,
      headers: {
        'content-type': 'text/html; charset=utf-8',
        'cache-control': 'no-store, max-age=0',
        'x-gv-sandbox': 'triangle-consensus-0006'
      }
    });
  }
};
