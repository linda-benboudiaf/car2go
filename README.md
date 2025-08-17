# Car2Go Backend

## Configuration

Create a `.env` file in the project root by copying `.env.example`:

```bash
cp .env.example .env
```

Then fill in the following variables:

- `DATABASE_URL`: Database connection string.
- `JWT_SECRET_KEY`: Secret key used to sign JWT tokens.
- `JWT_ALGORITHM`: Algorithm used for JWT tokens.
- `CORS_ORIGINS`: Comma-separated list of allowed origins for CORS.

The application will load these settings automatically when it starts.
