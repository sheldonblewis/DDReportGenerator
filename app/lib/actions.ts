'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { signIn } from '@/auth';
import { AuthError } from 'next-auth';

const FormSchema = z.object({
  id: z.string(),
  incomeStatement: z.any({
    invalid_type_error: 'Please select an income statement.',
  }),
  balanceSheet: z.any({
    invalid_type_error: 'Please select a balance sheet.',
  }),
  cashFlowStatement: z.any({
    invalid_type_error: 'Please select a cash flow statement.',
  }),
  date: z.string(),
});

export type State = {
  errors?: {
    incomeStatement?: any[];
    balanceSheet?: any[];
    cashFlowStatement?: any[];
  };
  message?: string | null;
};

const CreateJob = FormSchema.omit({ id: true, date: true });

export async function createJob(prevState: State, formData: FormData) {
  // Validate form fields using Zod
  const validatedFields = CreateJob.safeParse({
    incomeStatement: formData.get('incomeStatement'),
    balanceSheet: formData.get('balanceSheet'),
    cashFlowStatement: formData.get('cashFlowStatement'),
  });
  
  // If form validation fails, return errors early. Otherwise, continue.
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
      message: 'Missing Fields. Failed to Create Job.',
    };
  }
  

  // Prepare data for insertion into the database
  const { incomeStatement, balanceSheet, cashFlowStatement } = validatedFields.data;
  const date = new Date().toISOString().split('T')[0];

  const encodedIncomeStatement = encodeURIComponent(incomeStatement.name);
  const encodedBalanceSheet = encodeURIComponent(balanceSheet.name);
  const encodedCfStatement = encodeURIComponent(cashFlowStatement.name);

  revalidatePath(`/dashboard/due-diligence-report?income_statement=${encodedIncomeStatement}&balance_sheet=${encodedBalanceSheet}&cf_statement=${encodedCfStatement}`);
  redirect(`/dashboard/due-diligence-report?income_statement=${encodedIncomeStatement}&balance_sheet=${encodedBalanceSheet}&cf_statement=${encodedCfStatement}`);
  
  // Insert data into the database
  // try {
  //   await sql`
  //     INSERT INTO jobs (customer_id, amount, status, date)
  //     VALUES (${customerId}, ${amountInCents}, ${status}, ${date})
  //   `;
  // } catch (error) {
  //   // If a database error occurs, return a more specific error.
  //   return {
  //     message: 'Database Error: Failed to Create Job.',
  //   };
  // }

  // Revalidate the cache for the invoices page and redirect the user.
  // revalidatePath('/dashboard/');
  // redirect('/dashboard/');
}


export async function authenticate(
  prevState: string | undefined,
  formData: FormData,
) {
  try {
    await signIn('credentials', formData);
  } catch (error) {
    if (error instanceof AuthError) {
      switch (error.type) {
        case 'CredentialsSignin':
          return 'Invalid credentials.';
        default:
          return 'Something went wrong.';
      }
    }
    throw error;
  }
}