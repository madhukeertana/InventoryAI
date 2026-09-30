import { type FormEvent, useState } from "react";
import { CheckCircle2 } from "lucide-react";
import { api, ApiError } from "../api/client";
import { PageHeader } from "../components/ui/PageHeader";
import { Button } from "../components/ui/Button";
import { LoadingOverlay } from "../components/feedback/Spinner";
import { navIcons, Snowflake } from "../icons";
import type { InvoiceUploadResult } from "../types";

export function OcrPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<InvoiceUploadResult | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!file) {
      setError("Choose an invoice image or PDF");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const form = new FormData();
      form.append("file", file);
      const data = await api<InvoiceUploadResult>("/api/v1/ocr/invoices", {
        method: "POST",
        body: form,
      });
      setResult(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative">
      <PageHeader
        icon={navIcons.ocr}
        title="Inward OCR"
        subtitle="Scan supplier bills — batch, expiry, and cold-chain tags without slow manual entry."
      />
      {loading && <LoadingOverlay message="Parsing invoice…" />}
      {error && (
        <p className="mb-4 rounded-lg bg-surface-elevated px-3 py-2 text-sm ring-1 ring-primary-30" role="alert">
          {error}
        </p>
      )}

      <form
        onSubmit={onSubmit}
        className="rounded-2xl bg-surface-elevated p-5 ring-1 ring-primary-30"
      >
        <label className="flex flex-col gap-2 text-sm font-medium">
          Invoice file
          <input
            type="file"
            accept="image/*,.pdf"
            onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            className="block w-full text-sm text-primary-80 file:mr-3 file:rounded-lg file:border-0 file:bg-primary file:px-3 file:py-2 file:text-sm file:font-semibold file:text-surface"
          />
        </label>
        <p className="mt-2 text-xs text-primary-60">
          Tip: include “cold” in the filename to demo 2–8°C auto-tagging (OCR stub).
        </p>
        <Button className="mt-4" type="submit" loading={loading} icon={navIcons.ocr}>
          Upload &amp; parse
        </Button>
      </form>

      {result && (
        <div className="mt-6 rounded-2xl bg-surface-elevated p-5 ring-1 ring-primary-30">
          <p className="flex items-center gap-2 text-sm font-semibold">
            <CheckCircle2 className="h-4 w-4" aria-hidden />
            Parsed ({result.parse_status})
          </p>
          <pre className="mt-3 overflow-x-auto rounded-xl bg-surface p-3 text-xs text-primary-80">
            {JSON.stringify(result.parsed_payload, null, 2)}
          </pre>
          {result.created_batches.map((b) => (
            <p key={b.id} className="mt-3 flex items-center gap-2 text-sm text-primary-80">
              Created batch {b.batch_no} — qty {b.quantity}
              {b.cold_chain_flag && <Snowflake className="h-4 w-4" aria-label="Cold chain" />}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
