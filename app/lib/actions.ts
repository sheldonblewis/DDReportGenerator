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
      message: 'Missing Fields. Failed to Create Invoice.',
    };
  }

  // Prepare data for insertion into the database
  const { incomeStatement, balanceSheet, cashFlowStatement } = validatedFields.data;
  const date = new Date().toISOString().split('T')[0];

  const encodedIncomeStatement = encodeURIComponent(incomeStatement.name);
  const encodedBalanceSheet = encodeURIComponent(balanceSheet.name);
  const encodedCfStatement = encodeURIComponent(cashFlowStatement.name);
  console.log('------ income statement ------');
  console.log(incomeStatement);
  console.log(encodedIncomeStatement);

  // if (incomeStatement || balanceSheet || cashFlowStatement) {
    // wixLocation.to(`/due-diligence-report-page?income_statement=${encodedIncomeStatement}&balance_sheet=${encodedBalanceSheet}&cf_statement=${encodedCfStatement}`);
    revalidatePath(`/due-diligence-report-page?income_statement=${encodedIncomeStatement}&balance_sheet=${encodedBalanceSheet}&cf_statement=${encodedCfStatement}`);
    redirect(`/due-diligence-report-page?income_statement=${encodedIncomeStatement}&balance_sheet=${encodedBalanceSheet}&cf_statement=${encodedCfStatement}`);
  // }
  
  // Insert data into the database
  // try {
  //   await sql`
  //     INSERT INTO invoices (customer_id, amount, status, date)
  //     VALUES (${customerId}, ${amountInCents}, ${status}, ${date})
  //   `;
  // } catch (error) {
  //   // If a database error occurs, return a more specific error.
  //   return {
  //     message: 'Database Error: Failed to Create Invoice.',
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
    console.log(`trying to sign in ${formData}`);
    console.log(`
    user: 'postgres' \n
    password: ${process.env.NEXT_PUBLIC_POSTGRES_PASSWORD} \n
    host: ${process.env.NEXT_PUBLIC_POSTGRES_HOST} \n
    port: 5432 \n
    database: 'postgres' \n
    auth_url: ${process.env.NEXTAUTH_URL} \n
    auth_secret: ${process.env.NEXTAUTH_SECRET}`);
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