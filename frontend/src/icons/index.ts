import {
  AlertCircle,
  ArrowUpCircle,
  ClipboardList,
  LayoutDashboard,
  LogIn,
  LogOut,
  Package,
  Pill,
  ScanLine,
  ShieldAlert,
  ShoppingCart,
  Snowflake,
  Truck,
  Undo2,
  User,
  type LucideIcon,
} from "lucide-react";
import type { ActionCardType, Role } from "../types";

export const navIcons = {
  actions: ClipboardList,
  inventory: Package,
  ocr: ScanLine,
  profile: User,
  dashboard: LayoutDashboard,
  login: LogIn,
  logout: LogOut,
} as const;

export const actionCardIcons: Record<string, LucideIcon> = {
  ORDER: ShoppingCart,
  SELL_FIRST: ArrowUpCircle,
  RETURN: Undo2,
  TRANSFER: Truck,
  LICENSE_ALERT: ShieldAlert,
};

export function getActionIcon(type: ActionCardType | string): LucideIcon {
  return actionCardIcons[type] ?? AlertCircle;
}

export const roleLabels: Record<Role, string> = {
  PHARMACY_OWNER: "Pharmacy Owner",
  STORE_MANAGER: "Store Manager",
  PROCUREMENT_MANAGER: "Procurement Manager",
  HOSPITAL_INCHARGE: "Hospital In-charge",
  WAREHOUSE_BRANCH_MANAGER: "Warehouse / Branch Manager",
  MULTI_OUTLET_INVENTORY_HEAD: "Multi-outlet Inventory Head",
  SYSTEM_ADMIN: "System Admin",
};

export { Pill, Snowflake, AlertCircle };
