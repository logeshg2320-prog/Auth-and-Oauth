import axios from "axios";
const apiClient=axios.create({baseURL:import.meta.env.VITE_API_URL||"http://127.0.0.1:8000"});
apiClient.interceptors.request.use(c=>{const t=localStorage.getItem("access_token");if(t)c.headers.Authorization=`Bearer ${t}`;return c});
export default apiClient;