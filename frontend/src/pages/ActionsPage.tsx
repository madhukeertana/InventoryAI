import { useCallback, useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Inbox } from "lucide-react";
import { api, ApiError } from "../api/client";
import { PageHeader } from "../components/ui/PageHeader";
import { Button } from "../components/ui/Button";
import { EmptyState } from "../components/ui/EmptyState";
import { LoadingOverlay } from "../components/feedback/Spinner";
import { getActionIcon, navIcons } from "../icons";
import type { ActionCard } from "../types";

export function ActionsPage() {
  const [cards, setCards] = useState<ActionCard[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [busyId, setBusyId] = useState<string | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api<ActionCard[]>("/api/v1/action-cards/today");
      setCards(data);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to load actions");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void load();
  }, [load]);

  async function updateStatus(id: string, status: "ACCEPTED" | "OVERRIDDEN") {
    setBusyId(id);
    try {
      const updated = await api<ActionCard>(`/api/v1/action-cards/${id}`, {
        method: "PATCH",
        body: JSON.stringify({ status }),
      });
      setCards((prev) => prev.map((c) => (c.id === id ? updated : c)));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Update failed");
    } finally {
      setBusyId(null);
    }
  }

  return (
    <div className="relative">
      <PageHeader
        icon={navIcons.actions}
        title="Today's Actions"
        subtitle="Order, sell-first, transfer, return, and license alerts — with a reason you can defend."
      />
      {loading && <LoadingOverlay message="Loading today's action cards…" />}
      {error && (
        <p className="mb-4 rounded-lg bg-surface-elevated px-3 py-2 text-sm ring-1 ring-primary-30" role="alert">
          {error}
        </p>
      )}
      {!loading && cards.length === 0 ? (
        <EmptyState
          icon={Inbox}
          title="No actions right now"
          description="When stock, expiry, or license rules fire, your daily action cards will appear here."
        />
      ) : (
        <ul className="space-y-3">
          {cards.map((card, index) => {
            const Icon = getActionIcon(card.card_type);
            return (
              <motion.li
                key={card.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: Math.min(index * 0.04, 0.4) }}
                className="rounded-2xl bg-surface-elevated p-4 ring-1 ring-primary-30"
              >
                <div className="flex items-start gap-3">
                  <span className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-primary text-surface">
                    <Icon className="h-5 w-5" aria-hidden />
                  </span>
                  <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <p className="text-sm font-semibold uppercase tracking-wide text-primary">
                        {card.card_type.replace("_", " ")}
                      </p>
                      <span className="rounded-full bg-surface px-2 py-0.5 text-xs text-primary-80">
                        {card.status}
                      </span>
                    </div>
                    <p className="mt-1 text-sm text-primary-80">{card.reason}</p>
                    {card.status === "PENDING" && (
                      <div className="mt-3 flex flex-wrap gap-2">
                        <Button
                          loading={busyId === card.id}
                          icon={Icon}
                          onClick={() => updateStatus(card.id, "ACCEPTED")}
                        >
                          Accept
                        </Button>
                        <Button
                          variant="outline"
                          loading={busyId === card.id}
                          onClick={() => updateStatus(card.id, "OVERRIDDEN")}
                        >
                          Override
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
              </motion.li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
