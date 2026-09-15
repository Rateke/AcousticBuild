import axios from 'axios';

// Em desenvolvimento o back-end roda em localhost:8000. Publicado na Vercel,
// front e back dividem o mesmo domínio e a API responde em /api.
// VITE_API_URL, quando definido, tem prioridade sobre os dois.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
    || (import.meta.env.PROD ? '/api' : 'http://127.0.0.1:8000'),
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('acousticbuild_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Métodos auxiliares da Calculadora e Catálogo Construtivo
export const getMateriais = (categoria) =>
  api.get('/materiais', { params: categoria ? { categoria } : {} });

export const getSistemas = (tipoElemento) =>
  api.get('/sistemas', { params: tipoElemento ? { tipo_elemento: tipoElemento } : {} });

export const montarSistema = (camadas) =>
  api.post('/sistemas/montar', { camadas });

export const getCenarios = () =>
  api.get('/acustica/cenarios');

export default api;