export type Role =
  | "PHARMACY_OWNER"
  | "STORE_MANAGER"
  | "PROCUREMENT_MANAGER"
  | "HOSPITAL_INCHARGE"
  | "WAREHOUSE_BRANCH_MANAGER"
  | "MULTI_OUTLET_INVENTORY_HEAD"
  | "SYSTEM_ADMIN";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: Role;
  organization_id: string | null;
  location_id: string | null;
  is_active: boolean;
}

export interface Medicine {
  id: string;
  organization_id: string;
  name: string;
  sku: string;
  requires_cold_chain: boolean;
}

export interface StockBatch {
  id: string;
  medicine_id: string;
  location_id: string;
  batch_no: string;
  expiry_date: string;
  quantity: number;
  cold_chain_flag: boolean;
  velocity_tag: string | null;
  medicine_name?: string | null;
  location_name?: string | null;
}

export type ActionCardType =
  | "ORDER"
  | "SELL_FIRST"
  | "RETURN"
  | "TRANSFER"
  | "LICENSE_ALERT";

export interface ActionCard {
  id: string;
  organization_id: string;
  assignee_user_id: string | null;
  card_type: ActionCardType | string;
  status: string;
  reason: string;
  payload: Record<string, unknown> | null;
  action_date: string;
}

export interface InvoiceUploadResult {
  id: string;
  organization_id: string;
  uploaded_by: string;
  file_path: string;
  parse_status: string;
  parsed_payload: Record<string, unknown> | null;
  created_batches: StockBatch[];
}
