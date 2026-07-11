export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (!url.pathname.includes(".") && !url.pathname.endsWith("/")) {
      url.pathname = `${url.pathname}/`;
      return Response.redirect(url.toString(), 308);
    }

    const response = await env.ASSETS.fetch(request);
    if (response.status !== 404) {
      return response;
    }

    const fallback = new URL(request.url);
    fallback.pathname = "/index.html";
    return env.ASSETS.fetch(new Request(fallback, request));
  },
};
