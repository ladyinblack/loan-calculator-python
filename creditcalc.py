import math
import argparse

# declare parameters
parser = argparse.ArgumentParser(description="This program calculates your differentiated or annuity loan calculation.")

parser.add_argument("-t", "--type", choices=["annuity", "diff"], help="Incorrect parameters")
parser.add_argument("-pm", "--payment", help="Incorrect parameters")
parser.add_argument("-pn", "--principal")
parser.add_argument("-pd", "--periods")
parser.add_argument("-ist", "--interest", help="Incorrect parameters")


# calculate nominal interest which is 1/12th of the annual interest rate
def nominal_interest(ist):
    return (ist / 100) / 12


# calculate the number of months which is based on its nominal interest and loan principal
def number_of_months(ist, month_pay, ppl):
    nom_interest = nominal_interest(ist)
    return math.ceil(math.log(month_pay / (month_pay - nom_interest * ppl), 1 + nom_interest))


# calculate annuity over principal
def annuity_over_principal(ist, prd):
    nom_interest = nominal_interest(ist)
    return (math.pow(1 + nom_interest, prd) * nom_interest) / (math.pow(1 + nom_interest, prd) - 1)


# calculate the annuity payment given the nominal interest and the loan principal and the period
def calculated_annuity(ist, prd, ppl):
    a_over_p = annuity_over_principal(ist, prd)
    return ppl * a_over_p


# calculate the loan principal given the nominal interest and the annuity payment and period
def calculated_principal(ist, prd, ant):
    a_over_p = annuity_over_principal(ist, prd)
    return ant / a_over_p


# calculate differentiated payment given the principal, the count of periods, and interest
def differentiated_payment(pn, ist, pd, rm):
    nom_interest = nominal_interest(ist)
    return (pn / pd) + nom_interest * (pn - (pn * (rm - 1)) / pd)


# calculate total sum of payments
def total_sum_of_payments(pm, pd):
    tot_sum = 0
    for i in range(pd):
        tot_sum += pm
    return tot_sum


args = parser.parse_args()

if args.type == "annuity":
    # print(args.principal)
    # print(args.type)
    # print(args.payment)
    # print(args.periods)
    # print(args.interest)
    if args.principal is None and args.payment is not None and args.periods is not None and args.interest is not None:
        principal = calculated_principal(float(args.interest), int(args.periods), int(args.payment))
        print("Your loan principal = " + str(math.floor(principal)) + "!")
        print("Overpayment =", math.ceil(total_sum_of_payments(int(args.payment), int(args.periods)) - principal))
    elif args.payment is None and args.principal is not None and args.periods is not None and args.interest is not None:
        payment = math.ceil(calculated_annuity(float(args.interest), int(args.periods), int(args.principal)))
        print("Your annuity payment =", str(payment), "!")
        print("Overpayment =", total_sum_of_payments(payment, int(args.periods)) - int(args.principal))
    elif args.periods is None and args.principal is not None and args.payment is not None and args.interest is not None:
        periods = number_of_months(float(args.interest), int(args.payment), int(args.principal))
        years = math.floor(periods / 12)
        months = periods % 12
        if months == 0:
            print("It will take", years, "years to repay this loan!")
        elif months > 0:
            print("It will take", years, "years and", months, "months to repay this loan!")
        print("Overpayment =", total_sum_of_payments(int(args.payment), periods) - int(args.principal))
    else:
        print("Incorrect parameters")
elif args.type == "diff":
    if args.payment is None:
        tot_sum = 0
        for m in range(1, int(args.periods) + 1):
            payment = math.ceil(differentiated_payment(int(args.principal), float(args.interest), int(args.periods), m))
            tot_sum += payment
            print("Month " + str(m) + ": payment is " + str(payment))
        print("Overpayment =", tot_sum - int(args.principal))
    else:
        print("Incorrect parameters")
else:
    print("Incorrect parameters")


# print(args.type)
