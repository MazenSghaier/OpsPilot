import type { QueryKey, UseMutationOptions, UseMutationResult, UseQueryOptions, UseQueryResult } from "@tanstack/react-query";
import type { AlertFeedbackBody, AlertListResult, AlertRule, CreateJiraTicketBody, CreateRuleBody, DashboardStats, ErrorResult, FeedbackResult, FeedbackSummary, ForecastResult, GetAlertsParams, GetRuleViolationsParams, HealthStatus, IngestMetricsBody, IngestResult, JiraTicketResult, LoginBody, LoginResult, PredictServiceParams, RefreshTokenBody, RuleListResult, ServicesResult, UpdateRuleBody, ViolationListResult } from "./api.schemas";
import { customFetch } from "../custom-fetch";
import type { ErrorType, BodyType } from "../custom-fetch";
type AwaitedInput<T> = PromiseLike<T> | T;
type Awaited<O> = O extends AwaitedInput<infer T> ? T : never;
type SecondParameter<T extends (...args: never) => unknown> = Parameters<T>[1];
/**
 * Returns server health status
 * @summary Health check
 */
export declare const getHealthCheckUrl: () => string;
export declare const healthCheck: (options?: RequestInit) => Promise<HealthStatus>;
export declare const getHealthCheckQueryKey: () => readonly ["/api/healthz"];
export declare const getHealthCheckQueryOptions: <TData = Awaited<ReturnType<typeof healthCheck>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData> & {
    queryKey: QueryKey;
};
export type HealthCheckQueryResult = NonNullable<Awaited<ReturnType<typeof healthCheck>>>;
export type HealthCheckQueryError = ErrorType<unknown>;
/**
 * @summary Health check
 */
export declare function useHealthCheck<TData = Awaited<ReturnType<typeof healthCheck>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof healthCheck>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * Detects anomalies and triggers background alerting tasks
 * @summary Ingest infrastructure metrics
 */
export declare const getIngestMetricsUrl: () => string;
export declare const ingestMetrics: (ingestMetricsBody: IngestMetricsBody, options?: RequestInit) => Promise<IngestResult>;
export declare const getIngestMetricsMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof ingestMetrics>>, TError, {
        data: BodyType<IngestMetricsBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof ingestMetrics>>, TError, {
    data: BodyType<IngestMetricsBody>;
}, TContext>;
export type IngestMetricsMutationResult = NonNullable<Awaited<ReturnType<typeof ingestMetrics>>>;
export type IngestMetricsMutationBody = BodyType<IngestMetricsBody>;
export type IngestMetricsMutationError = ErrorType<unknown>;
/**
 * @summary Ingest infrastructure metrics
 */
export declare const useIngestMetrics: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof ingestMetrics>>, TError, {
        data: BodyType<IngestMetricsBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof ingestMetrics>>, TError, {
    data: BodyType<IngestMetricsBody>;
}, TContext>;
/**
 * @summary Get recent alerts
 */
export declare const getGetAlertsUrl: (params?: GetAlertsParams) => string;
export declare const getAlerts: (params?: GetAlertsParams, options?: RequestInit) => Promise<AlertListResult>;
export declare const getGetAlertsQueryKey: (params?: GetAlertsParams) => readonly ["/api/alerts", ...GetAlertsParams[]];
export declare const getGetAlertsQueryOptions: <TData = Awaited<ReturnType<typeof getAlerts>>, TError = ErrorType<unknown>>(params?: GetAlertsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getAlerts>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getAlerts>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetAlertsQueryResult = NonNullable<Awaited<ReturnType<typeof getAlerts>>>;
export type GetAlertsQueryError = ErrorType<unknown>;
/**
 * @summary Get recent alerts
 */
export declare function useGetAlerts<TData = Awaited<ReturnType<typeof getAlerts>>, TError = ErrorType<unknown>>(params?: GetAlertsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getAlerts>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Submit feedback on an alert
 */
export declare const getSubmitAlertFeedbackUrl: (id: string) => string;
export declare const submitAlertFeedback: (id: string, alertFeedbackBody: AlertFeedbackBody, options?: RequestInit) => Promise<FeedbackResult>;
export declare const getSubmitAlertFeedbackMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof submitAlertFeedback>>, TError, {
        id: string;
        data: BodyType<AlertFeedbackBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof submitAlertFeedback>>, TError, {
    id: string;
    data: BodyType<AlertFeedbackBody>;
}, TContext>;
export type SubmitAlertFeedbackMutationResult = NonNullable<Awaited<ReturnType<typeof submitAlertFeedback>>>;
export type SubmitAlertFeedbackMutationBody = BodyType<AlertFeedbackBody>;
export type SubmitAlertFeedbackMutationError = ErrorType<unknown>;
/**
 * @summary Submit feedback on an alert
 */
export declare const useSubmitAlertFeedback: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof submitAlertFeedback>>, TError, {
        id: string;
        data: BodyType<AlertFeedbackBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof submitAlertFeedback>>, TError, {
    id: string;
    data: BodyType<AlertFeedbackBody>;
}, TContext>;
/**
 * @summary Get feedback accuracy summary
 */
export declare const getGetFeedbackSummaryUrl: () => string;
export declare const getFeedbackSummary: (options?: RequestInit) => Promise<FeedbackSummary>;
export declare const getGetFeedbackSummaryQueryKey: () => readonly ["/api/feedback/summary"];
export declare const getGetFeedbackSummaryQueryOptions: <TData = Awaited<ReturnType<typeof getFeedbackSummary>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getFeedbackSummary>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getFeedbackSummary>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetFeedbackSummaryQueryResult = NonNullable<Awaited<ReturnType<typeof getFeedbackSummary>>>;
export type GetFeedbackSummaryQueryError = ErrorType<unknown>;
/**
 * @summary Get feedback accuracy summary
 */
export declare function useGetFeedbackSummary<TData = Awaited<ReturnType<typeof getFeedbackSummary>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getFeedbackSummary>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Get metric forecast for a service
 */
export declare const getPredictServiceUrl: (service: string, params?: PredictServiceParams) => string;
export declare const predictService: (service: string, params?: PredictServiceParams, options?: RequestInit) => Promise<ForecastResult>;
export declare const getPredictServiceQueryKey: (service: string, params?: PredictServiceParams) => readonly [`/api/predict/${string}`, ...PredictServiceParams[]];
export declare const getPredictServiceQueryOptions: <TData = Awaited<ReturnType<typeof predictService>>, TError = ErrorType<unknown>>(service: string, params?: PredictServiceParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof predictService>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof predictService>>, TError, TData> & {
    queryKey: QueryKey;
};
export type PredictServiceQueryResult = NonNullable<Awaited<ReturnType<typeof predictService>>>;
export type PredictServiceQueryError = ErrorType<unknown>;
/**
 * @summary Get metric forecast for a service
 */
export declare function usePredictService<TData = Awaited<ReturnType<typeof predictService>>, TError = ErrorType<unknown>>(service: string, params?: PredictServiceParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof predictService>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Get list of known services with alert counts
 */
export declare const getGetServicesUrl: () => string;
export declare const getServices: (options?: RequestInit) => Promise<ServicesResult>;
export declare const getGetServicesQueryKey: () => readonly ["/api/services"];
export declare const getGetServicesQueryOptions: <TData = Awaited<ReturnType<typeof getServices>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getServices>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getServices>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetServicesQueryResult = NonNullable<Awaited<ReturnType<typeof getServices>>>;
export type GetServicesQueryError = ErrorType<unknown>;
/**
 * @summary Get list of known services with alert counts
 */
export declare function useGetServices<TData = Awaited<ReturnType<typeof getServices>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getServices>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Get dashboard KPI statistics
 */
export declare const getGetDashboardStatsUrl: () => string;
export declare const getDashboardStats: (options?: RequestInit) => Promise<DashboardStats>;
export declare const getGetDashboardStatsQueryKey: () => readonly ["/api/dashboard/stats"];
export declare const getGetDashboardStatsQueryOptions: <TData = Awaited<ReturnType<typeof getDashboardStats>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getDashboardStats>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getDashboardStats>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetDashboardStatsQueryResult = NonNullable<Awaited<ReturnType<typeof getDashboardStats>>>;
export type GetDashboardStatsQueryError = ErrorType<unknown>;
/**
 * @summary Get dashboard KPI statistics
 */
export declare function useGetDashboardStats<TData = Awaited<ReturnType<typeof getDashboardStats>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getDashboardStats>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Create a Jira ticket for an incident
 */
export declare const getCreateJiraTicketUrl: () => string;
export declare const createJiraTicket: (createJiraTicketBody: CreateJiraTicketBody, options?: RequestInit) => Promise<JiraTicketResult>;
export declare const getCreateJiraTicketMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createJiraTicket>>, TError, {
        data: BodyType<CreateJiraTicketBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof createJiraTicket>>, TError, {
    data: BodyType<CreateJiraTicketBody>;
}, TContext>;
export type CreateJiraTicketMutationResult = NonNullable<Awaited<ReturnType<typeof createJiraTicket>>>;
export type CreateJiraTicketMutationBody = BodyType<CreateJiraTicketBody>;
export type CreateJiraTicketMutationError = ErrorType<unknown>;
/**
 * @summary Create a Jira ticket for an incident
 */
export declare const useCreateJiraTicket: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createJiraTicket>>, TError, {
        data: BodyType<CreateJiraTicketBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof createJiraTicket>>, TError, {
    data: BodyType<CreateJiraTicketBody>;
}, TContext>;
/**
 * @summary Login and get JWT tokens
 */
export declare const getLoginUrl: () => string;
export declare const login: (loginBody: LoginBody, options?: RequestInit) => Promise<LoginResult>;
export declare const getLoginMutationOptions: <TError = ErrorType<ErrorResult>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof login>>, TError, {
        data: BodyType<LoginBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof login>>, TError, {
    data: BodyType<LoginBody>;
}, TContext>;
export type LoginMutationResult = NonNullable<Awaited<ReturnType<typeof login>>>;
export type LoginMutationBody = BodyType<LoginBody>;
export type LoginMutationError = ErrorType<ErrorResult>;
/**
 * @summary Login and get JWT tokens
 */
export declare const useLogin: <TError = ErrorType<ErrorResult>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof login>>, TError, {
        data: BodyType<LoginBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof login>>, TError, {
    data: BodyType<LoginBody>;
}, TContext>;
/**
 * @summary Refresh access token
 */
export declare const getRefreshTokenUrl: () => string;
export declare const refreshToken: (refreshTokenBody: RefreshTokenBody, options?: RequestInit) => Promise<LoginResult>;
export declare const getRefreshTokenMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof refreshToken>>, TError, {
        data: BodyType<RefreshTokenBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof refreshToken>>, TError, {
    data: BodyType<RefreshTokenBody>;
}, TContext>;
export type RefreshTokenMutationResult = NonNullable<Awaited<ReturnType<typeof refreshToken>>>;
export type RefreshTokenMutationBody = BodyType<RefreshTokenBody>;
export type RefreshTokenMutationError = ErrorType<unknown>;
/**
 * @summary Refresh access token
 */
export declare const useRefreshToken: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof refreshToken>>, TError, {
        data: BodyType<RefreshTokenBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof refreshToken>>, TError, {
    data: BodyType<RefreshTokenBody>;
}, TContext>;
/**
 * @summary List all alert rules
 */
export declare const getGetRulesUrl: () => string;
export declare const getRules: (options?: RequestInit) => Promise<RuleListResult>;
export declare const getGetRulesQueryKey: () => readonly ["/api/rules"];
export declare const getGetRulesQueryOptions: <TData = Awaited<ReturnType<typeof getRules>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getRules>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getRules>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetRulesQueryResult = NonNullable<Awaited<ReturnType<typeof getRules>>>;
export type GetRulesQueryError = ErrorType<unknown>;
/**
 * @summary List all alert rules
 */
export declare function useGetRules<TData = Awaited<ReturnType<typeof getRules>>, TError = ErrorType<unknown>>(options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getRules>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
/**
 * @summary Create a new alert rule
 */
export declare const getCreateRuleUrl: () => string;
export declare const createRule: (createRuleBody: CreateRuleBody, options?: RequestInit) => Promise<AlertRule>;
export declare const getCreateRuleMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createRule>>, TError, {
        data: BodyType<CreateRuleBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof createRule>>, TError, {
    data: BodyType<CreateRuleBody>;
}, TContext>;
export type CreateRuleMutationResult = NonNullable<Awaited<ReturnType<typeof createRule>>>;
export type CreateRuleMutationBody = BodyType<CreateRuleBody>;
export type CreateRuleMutationError = ErrorType<unknown>;
/**
 * @summary Create a new alert rule
 */
export declare const useCreateRule: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof createRule>>, TError, {
        data: BodyType<CreateRuleBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof createRule>>, TError, {
    data: BodyType<CreateRuleBody>;
}, TContext>;
/**
 * @summary Update an alert rule
 */
export declare const getUpdateRuleUrl: (id: string) => string;
export declare const updateRule: (id: string, updateRuleBody: UpdateRuleBody, options?: RequestInit) => Promise<AlertRule>;
export declare const getUpdateRuleMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof updateRule>>, TError, {
        id: string;
        data: BodyType<UpdateRuleBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof updateRule>>, TError, {
    id: string;
    data: BodyType<UpdateRuleBody>;
}, TContext>;
export type UpdateRuleMutationResult = NonNullable<Awaited<ReturnType<typeof updateRule>>>;
export type UpdateRuleMutationBody = BodyType<UpdateRuleBody>;
export type UpdateRuleMutationError = ErrorType<unknown>;
/**
 * @summary Update an alert rule
 */
export declare const useUpdateRule: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof updateRule>>, TError, {
        id: string;
        data: BodyType<UpdateRuleBody>;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof updateRule>>, TError, {
    id: string;
    data: BodyType<UpdateRuleBody>;
}, TContext>;
/**
 * @summary Delete an alert rule
 */
export declare const getDeleteRuleUrl: (id: string) => string;
export declare const deleteRule: (id: string, options?: RequestInit) => Promise<FeedbackResult>;
export declare const getDeleteRuleMutationOptions: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof deleteRule>>, TError, {
        id: string;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationOptions<Awaited<ReturnType<typeof deleteRule>>, TError, {
    id: string;
}, TContext>;
export type DeleteRuleMutationResult = NonNullable<Awaited<ReturnType<typeof deleteRule>>>;
export type DeleteRuleMutationError = ErrorType<unknown>;
/**
 * @summary Delete an alert rule
 */
export declare const useDeleteRule: <TError = ErrorType<unknown>, TContext = unknown>(options?: {
    mutation?: UseMutationOptions<Awaited<ReturnType<typeof deleteRule>>, TError, {
        id: string;
    }, TContext>;
    request?: SecondParameter<typeof customFetch>;
}) => UseMutationResult<Awaited<ReturnType<typeof deleteRule>>, TError, {
    id: string;
}, TContext>;
/**
 * @summary Get recent rule violations
 */
export declare const getGetRuleViolationsUrl: (params?: GetRuleViolationsParams) => string;
export declare const getRuleViolations: (params?: GetRuleViolationsParams, options?: RequestInit) => Promise<ViolationListResult>;
export declare const getGetRuleViolationsQueryKey: (params?: GetRuleViolationsParams) => readonly ["/api/rules/violations", ...GetRuleViolationsParams[]];
export declare const getGetRuleViolationsQueryOptions: <TData = Awaited<ReturnType<typeof getRuleViolations>>, TError = ErrorType<unknown>>(params?: GetRuleViolationsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getRuleViolations>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}) => UseQueryOptions<Awaited<ReturnType<typeof getRuleViolations>>, TError, TData> & {
    queryKey: QueryKey;
};
export type GetRuleViolationsQueryResult = NonNullable<Awaited<ReturnType<typeof getRuleViolations>>>;
export type GetRuleViolationsQueryError = ErrorType<unknown>;
/**
 * @summary Get recent rule violations
 */
export declare function useGetRuleViolations<TData = Awaited<ReturnType<typeof getRuleViolations>>, TError = ErrorType<unknown>>(params?: GetRuleViolationsParams, options?: {
    query?: UseQueryOptions<Awaited<ReturnType<typeof getRuleViolations>>, TError, TData>;
    request?: SecondParameter<typeof customFetch>;
}): UseQueryResult<TData, TError> & {
    queryKey: QueryKey;
};
export {};
//# sourceMappingURL=api.d.ts.map