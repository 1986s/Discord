from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html data-bs-theme="dark">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Discord Moderation Bot</title>
        <link rel="stylesheet" href="https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css">
        <style>
            body {
                padding-top: 2rem;
            }
            .feature-icon {
                font-size: 2rem;
                margin-bottom: 1rem;
                color: var(--bs-primary);
            }
            .bot-card {
                border-radius: 1rem;
                overflow: hidden;
                transition: transform 0.3s ease;
            }
            .bot-card:hover {
                transform: translateY(-5px);
            }
        </style>
    </head>
    <body>
        <div class="container py-4">
            <header class="pb-3 mb-4 border-bottom">
                <div class="d-flex align-items-center">
                    <h1 class="fw-bold">Discord Moderation Bot</h1>
                    <span class="badge bg-primary ms-3">Online</span>
                </div>
                <p class="lead text-body-secondary">Advanced server protection with powerful moderation tools</p>
            </header>

            <div class="p-5 mb-4 bg-dark-subtle rounded-3">
                <div class="container-fluid py-3">
                    <h2 class="fw-bold mb-3">Bot Status</h2>
                    <p class="fs-5">Your Discord moderation bot is currently active and connected to Discord.</p>
                    <p>Use <code>/help</code> in your Discord server to see all available commands.</p>
                </div>
            </div>

            <div class="row row-cols-1 row-cols-md-2 g-4 mb-4">
                <div class="col">
                    <div class="card h-100 bot-card bg-dark-subtle">
                        <div class="card-body">
                            <div class="feature-icon">🛡️</div>
                            <h3 class="card-title">Moderation Commands</h3>
                            <p class="card-text">Comprehensive tools for server management including warnings, bans, kicks, and mutes.</p>
                            <ul class="list-group list-group-flush bg-transparent mb-3">
                                <li class="list-group-item bg-transparent border-secondary">/warn - Warn users</li>
                                <li class="list-group-item bg-transparent border-secondary">/kick - Remove users from server</li>
                                <li class="list-group-item bg-transparent border-secondary">/ban - Ban users from server</li>
                                <li class="list-group-item bg-transparent border-secondary">/mute - Timeout users</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card h-100 bot-card bg-dark-subtle">
                        <div class="card-body">
                            <div class="feature-icon">🤖</div>
                            <h3 class="card-title">Auto-Moderation</h3>
                            <p class="card-text">Automatic content filtering and protection against spam, profanity, and raids.</p>
                            <ul class="list-group list-group-flush bg-transparent mb-3">
                                <li class="list-group-item bg-transparent border-secondary">Profanity filter with bypass detection</li>
                                <li class="list-group-item bg-transparent border-secondary">Anti-spam protection</li>
                                <li class="list-group-item bg-transparent border-secondary">Mass mention prevention</li>
                                <li class="list-group-item bg-transparent border-secondary">Invite link blocking</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card h-100 bot-card bg-dark-subtle">
                        <div class="card-body">
                            <div class="feature-icon">📊</div>
                            <h3 class="card-title">Logging System</h3>
                            <p class="card-text">Comprehensive event tracking and recording for server transparency.</p>
                            <ul class="list-group list-group-flush bg-transparent mb-3">
                                <li class="list-group-item bg-transparent border-secondary">Message edits and deletions</li>
                                <li class="list-group-item bg-transparent border-secondary">User joins and leaves</li>
                                <li class="list-group-item bg-transparent border-secondary">Moderation actions</li>
                                <li class="list-group-item bg-transparent border-secondary">Role and channel changes</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col">
                    <div class="card h-100 bot-card bg-dark-subtle">
                        <div class="card-body">
                            <div class="feature-icon">👥</div>
                            <h3 class="card-title">Role Management</h3>
                            <p class="card-text">Automatic and bulk role assignment tools for efficient server organization.</p>
                            <ul class="list-group list-group-flush bg-transparent mb-3">
                                <li class="list-group-item bg-transparent border-secondary">Auto-role for new members</li>
                                <li class="list-group-item bg-transparent border-secondary">Mass role assignments</li>
                                <li class="list-group-item bg-transparent border-secondary">Role permission management</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <footer class="pt-3 mt-4 text-body-secondary border-top">
                <div class="d-flex justify-content-between align-items-center">
                    <span>Made with ❤️ by 30ax</span>
                    <span>Discord Moderation Bot &copy; 2025</span>
                </div>
            </footer>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)