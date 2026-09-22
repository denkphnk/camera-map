import { api } from "./axios";

import type { AnalysisFilters } from "../types/analysis.types";

export const analysisApi = {
  getAll(filters?: AnalysisFilters) {
    return api.get("/analyses", {
      params: filters,
    });
  },

  getById(id: string) {
    return api.get(`/analyses/${id}`);
  },
};