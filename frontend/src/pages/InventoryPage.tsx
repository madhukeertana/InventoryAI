import { type FormEvent, useCallback, useEffect, useState } from "react";
import { CalendarClock, Inbox } from "lucide-react";
import { api, ApiError } from "../api/client";
import { PageHeader } from "../components/ui/PageHeader";
import { Button } from "../components/ui/Button";
import { Input } from "../components/ui/Input";
import { EmptyState } from "../components/ui/EmptyState";
import { LoadingOverlay } from "../components/feedback/Spinner";
import { Pill, Snowflake, navIcons } from "../icons";
import type { Medicine, StockBatch } from "../types";

export function InventoryPage() {
  const [medicines, setMedicines] = useState<Medicine[]>([]);
  const [batches, setBatches] = useState<StockBatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [name, setName] = useState("");
  const [sku, setSku] = useState("");
  const [cold, setCold] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [meds, batchList] = await Promise.all([
        api<Medicine[]>("/api/v1/inventory/medicines"),
        api<StockBatch[]>("/api/v1/inventory/batches"),
      ]);
      setMedicines(meds);
      setBatches(batchList);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to load inventory");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  async function onCreateMedicine(e: FormEvent) {
    e.preventDefault();
    setSaving(true);
    setError(null);
    try {
      await api<Medicine>("/api/v1/inventory/medicines", {
        method: "POST",
        body: JSON.stringify({
          name,
          sku,
          requires_cold_chain: cold,
        }),
      });
      setName("");
      setSku("");
      setCold(false);
      await load();
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Create failed");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="relative">
      <PageHeader
        icon={navIcons.inventory}
        title="Inventory"
        subtitle="Batch, expiry, cold-chain, and velocity — scoped to your organization."
      />
      {loading && <LoadingOverlay message="Loading inventory…" />}
      {error && (
        <p className="mb-4 rounded-lg bg-surface-elevated px-3 py-2 text-sm ring-1 ring-primary-30" role="alert">
          {error}
        </p>
      )}

      <section className="mb-8 rounded-2xl bg-surface-elevated p-4 ring-1 ring-primary-30 md:p-5">
        <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide">
          <Pill className="h-4 w-4" aria-hidden />
          Add medicine
        </h2>
        <form className="grid gap-3 md:grid-cols-4 md:items-end" onSubmit={onCreateMedicine}>
          <Input label="Name" value={name} onChange={(e) => setName(e.target.value)} required />
          <Input label="SKU" value={sku} onChange={(e) => setSku(e.target.value)} required />
          <label className="flex items-center gap-2 pb-2 text-sm">
            <input
              type="checkbox"
              checked={cold}
              onChange={(e) => setCold(e.target.checked)}
              className="h-4 w-4 accent-primary"
            />
            <Snowflake className="h-4 w-4" aria-hidden />
            Cold chain 2–8°C
          </label>
          <Button type="submit" loading={saving} icon={Pill}>
            Save
          </Button>
        </form>
      </section>

      <section className="mb-8">
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-primary-80">
          Medicines ({medicines.length})
        </h2>
        {medicines.length === 0 && !loading ? (
          <EmptyState
            icon={Inbox}
            title="No medicines yet"
            description="Add a SKU or upload an invoice via Inward OCR."
          />
        ) : (
          <ul className="grid gap-3 sm:grid-cols-2">
            {medicines.map((m) => (
              <li
                key={m.id}
                className="flex items-start gap-3 rounded-xl bg-surface-elevated p-4 ring-1 ring-primary-30"
              >
                <Pill className="mt-0.5 h-5 w-5 shrink-0" aria-hidden />
                <div>
                  <p className="font-semibold">{m.name}</p>
                  <p className="text-sm text-primary-80">{m.sku}</p>
                  {m.requires_cold_chain && (
                    <p className="mt-1 flex items-center gap-1 text-xs text-primary-80">
                      <Snowflake className="h-3.5 w-3.5" aria-hidden />
                      Cold chain
                    </p>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section>
        <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-primary-80">
          <CalendarClock className="h-4 w-4" aria-hidden />
          Batches ({batches.length})
        </h2>
        <div className="overflow-hidden rounded-2xl ring-1 ring-primary-30">
          <div className="hidden bg-surface-elevated md:grid md:grid-cols-6 md:gap-2 md:px-4 md:py-3 md:text-xs md:font-semibold md:uppercase md:tracking-wide md:text-primary-80">
            <span>Medicine</span>
            <span>Batch</span>
            <span>Expiry</span>
            <span>Qty</span>
            <span>Velocity</span>
            <span>Flags</span>
          </div>
          <ul className="divide-y divide-primary-30 bg-surface-elevated">
            {batches.map((b) => (
              <li
                key={b.id}
                className="grid gap-1 px-4 py-3 text-sm md:grid-cols-6 md:items-center md:gap-2"
              >
                <span className="font-medium">{b.medicine_name ?? b.medicine_id}</span>
                <span className="text-primary-80">{b.batch_no}</span>
                <span className="text-primary-80">{b.expiry_date}</span>
                <span>{b.quantity}</span>
                <span className="text-primary-80">{b.velocity_tag ?? "—"}</span>
                <span className="flex items-center gap-2 text-primary-80">
                  {b.cold_chain_flag && <Snowflake className="h-4 w-4" aria-label="Cold chain" />}
                  <span className="md:hidden text-xs">{b.location_name}</span>
                </span>
              </li>
            ))}
          </ul>
        </div>
      </section>
    </div>
  );
}
