import { useState } from "react";
import { useServerSettings } from "../../hooks/useServerSettings";
import type { ServerSettings, ServerSettingsUpdate } from "../../types/server";
import styles from "./ServerSettingsPanel.module.css";

/**
 * Displays and manages the server's current settings.
 *
 * Retrieves the current settings from the backend and renders a form
 * that allows the user to update them.
 */
export function ServerSettingsPanel() {
    const {
        serverSettings,
        isLoading,
        isSaving,
        error,
        saveSettings,
    } = useServerSettings();

    if (isLoading) {
        return <div>Loading settings...</div>;
    }

    if (error) {
        return <div>{error}</div>;
    }

    if (!serverSettings) {
        return <div>No server settings available.</div>;
    }

    return (
        <div className={styles.settingsCard}>
            <h2 className={styles.centeredLine}>Server Settings</h2>

            <SettingsForm
                settings={serverSettings}
                onSubmit={saveSettings}
                isSaving={isSaving}
            />
        </div>
    );
}

interface SettingsFormProps {
    settings: ServerSettings;
    onSubmit: (settings: ServerSettingsUpdate) => Promise<void>;
    isSaving: boolean;
}

/**
 * Renders the editable server settings form.
 *
 * Initializes the form with the current server settings and submits
 * updated values through the provided `onSubmit` callback.
 */
function SettingsForm({ settings, onSubmit, isSaving }: SettingsFormProps) {
    const [refreshInterval, setRefreshInterval] = useState(settings.refresh_interval);
    const [weeksDelta, setWeeksDelta] = useState(settings.weeks_delta);

    const [canvasEnabled, setCanvasEnabled] = useState(settings.canvas.enabled);
    const [canvasGraphqlUrl, setCanvasGraphqlUrl] = useState(settings.canvas.graphql_url);
    const [canvasToken, setCanvasToken] = useState("")

    const [gradescopeEnabled, setGradescopeEnabled] = useState(settings.gradescope.enabled);
    const [gradescopeEmail, setGradescopeEmail] = useState(settings.gradescope.email);
    const [gradescopePassword, setGradescopePassword] = useState("")

    const [ngrokEnabled, setNgrokEnabled] = useState(settings.ngrok.enabled);
    const [ngrokDomain, setNgrokDomain] = useState(settings.ngrok.domain);
    const [ngrokToken, setNgrokToken] = useState("")

    /**
     * Prevents the browser's default form submission and sends the current
     * form values to the parent component for persistence.
     */
    function handleSubmit(event: React.SubmitEvent<HTMLFormElement>) {
        event.preventDefault();

        const newSettings: ServerSettingsUpdate = {
            refresh_interval: refreshInterval,
            weeks_delta: weeksDelta,

            canvas_enabled: canvasEnabled,
            canvas_graphql_url: canvasGraphqlUrl,
            canvas_token: canvasToken || undefined,

            gradescope_enabled: gradescopeEnabled,
            gradescope_email: gradescopeEmail,
            gradescope_password: gradescopePassword || undefined,

            ngrok_enabled: ngrokEnabled,
            ngrok_domain: ngrokDomain,
            ngrok_authtoken: ngrokToken || undefined,
        };

        void onSubmit(newSettings);
    }

    return (
        <form onSubmit={handleSubmit}>
            <h3>General:</h3>
            <label>
                Refresh Interval:{" "}
                <input
                    type="number"
                    value={refreshInterval}
                    onChange={(e) => setRefreshInterval(Number(e.target.value))}
                />
            </label>
            <br />
            <label>
                Weeks Delta:{" "}
                <input
                    type="number"
                    value={weeksDelta}
                    onChange={(e) => setWeeksDelta(Number(e.target.value))}
                />
            </label>

            <h3>Canvas:</h3>
            <label>
                Enabled:{" "}
                <input
                    type="checkbox"
                    checked={canvasEnabled}
                    onChange={(e) => setCanvasEnabled(e.target.checked)}
                />
            </label>
            <br />
            <label>
                GraphQL URL:{" "}
                <input
                    type="text"
                    value={canvasGraphqlUrl || ""}
                    onChange={(e) => setCanvasGraphqlUrl(e.target.value)}
                />
            </label>
            <br />
            <label>
                Authtoken:{" "}
                <input
                    type="password"
                    value={canvasToken}
                    placeholder={
                        settings.canvas.token_configured ? "Configured" : "Not configured"
                    }
                    onChange={(e) => setCanvasToken(e.target.value)}
                />
            </label>

            <h3>Gradescope:</h3>
            <label>
                Enabled:{" "}
                <input
                    type="checkbox"
                    checked={gradescopeEnabled}
                    onChange={(e) => setGradescopeEnabled(e.target.checked)}
                />
            </label>
            <br />
            <label>
                Email:{" "}
                <input
                    type="text"
                    value={gradescopeEmail || ""}
                    onChange={(e) => setGradescopeEmail(e.target.value)}
                />
            </label>
            <br />
            <label>
                Password:{" "}
                <input
                    type="password"
                    value={gradescopePassword}
                    placeholder={
                        settings.gradescope.password_configured ? "Configured" : "Not configured"
                    }
                    onChange={(e) => setGradescopePassword(e.target.value)}
                />
            </label>

            <h3>ngrok:</h3>
            <label>
                Enabled:{" "}
                <input
                    type="checkbox"
                    checked={ngrokEnabled}
                    onChange={(e) => setNgrokEnabled(e.target.checked)}
                />
            </label>
            <br />
            <label>
                Domain:{" "}
                <input
                    type="text"
                    value={ngrokDomain || ""}
                    onChange={(e) => setNgrokDomain(e.target.value)}
                />
            </label>
            <br />
            <label>
                Authtoken:{" "}
                <input
                    type="password"
                    value={ngrokToken}
                    placeholder={
                        settings.ngrok.authtoken_configured ? "Configured" : "Not configured"
                    }
                    onChange={(e) => setNgrokToken(e.target.value)}
                />
            </label>
            <br />
            <br />

            <button type="submit" disabled={isSaving}>
                {isSaving ? "Saving..." : "Save Settings"}
            </button>
        </form>
    );
}