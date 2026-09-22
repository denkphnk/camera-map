import { useQuery } from "@tanstack/react-query";

import { analysisApi } from "../api/analysis.api";
import type { AnalysisFilters, AnalysisListResponse } from "../types/analysis.types";

export function useAnalyses(
  filters: AnalysisFilters = {},
) {
  return useQuery<AnalysisListResponse>({
    queryKey: [
      "analyses",
      filters,
    ],

    queryFn: async () => {
      const response =
        await analysisApi.getAll(
          filters,
        );

      return response.data;
    },

    refetchInterval: 3000,
  });
}

