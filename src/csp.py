"""Content-Security-Policy and the other security headers. One place, used by Flask (dynamic pages) and mirrored in
vercel.json for static files (a test keeps the two in step).

Pages: only our own scripts, the Google Fonts stylesheet and font files, our own self-hosted font (Atkinson Hyperlegible), inline styles (the templates use style
attributes), data: images (the favicon). Nothing else is allowed to load or connect.

The code runner (public/static/runner.js) runs in a Web Worker and gets its own, wider policy because the worker's
policy comes from the response that served the worker script: it needs `new Function` (learner JavaScript),
WebAssembly (Python via Pyodide) and the one CDN that serves Pyodide.
"""

PAGE_CSP = ("default-src 'self'; script-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data:; connect-src 'self'; worker-src 'self'; object-src 'none'; "
            "base-uri 'self'; form-action 'self'; frame-ancestors 'none'")

RUNNER_CSP = ("default-src 'none'; script-src 'self' https://cdn.jsdelivr.net 'unsafe-eval' 'wasm-unsafe-eval'; "
              "connect-src https://cdn.jsdelivr.net; frame-ancestors 'none'")

RUNNER_PATH = "/static/runner.js"

COMMON = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "no-referrer",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}


def headers_for(path):
    """Security headers for a response to `path`."""
    return {**COMMON, "Content-Security-Policy": RUNNER_CSP if path == RUNNER_PATH else PAGE_CSP}
