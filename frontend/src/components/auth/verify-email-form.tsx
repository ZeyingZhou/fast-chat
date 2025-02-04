'use client';

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { verifyEmail } from '@/actions/auth';

export function VerifyEmailForm() {
  const router = useRouter();
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  const onSubmit = async () => {
    if (!token) {
      setError('Invalid verification link');
      return;
    }

    try {
      setLoading(true);
      await verifyEmail(token);
      router.push('/auth/login?verified=true');
    } catch (err) {
      setError('Failed to verify email. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col space-y-4">
      <h1 className="text-2xl font-semibold tracking-tight">
        Verify your email
      </h1>
      {error && (
        <p className="text-sm text-red-500">
          {error}
        </p>
      )}
      <button
        onClick={onSubmit}
        disabled={loading || !token}
        className="inline-flex w-full items-center justify-center rounded-lg bg-primary px-5 py-2.5 text-center text-sm font-medium text-white hover:bg-primary/90 disabled:opacity-50"
      >
        {loading ? 'Verifying...' : 'Verify Email'}
      </button>
    </div>
  );
} 