/*********************************************************************
 *
 *                UBW Firmware
 *
 *********************************************************************
 * FileName:        UBW.h
 * Company:         Schmalz Haus LLC
 * Author:          Brian Schmalz
 *
 * Based on original files by Microchip Inc. in MAL USB example.
 *
 * Software License Agreement
 *
 * Copyright (c) 2014-2023, Brian Schmalz of Schmalz Haus LLC
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or
 * without modification, are permitted provided that the following
 * conditions are met:
 *
 * 1. Redistributions of source code must retain the above
 * copyright notice, this list of conditions and the following
 * disclaimer.
 *
 * 2. Redistributions in binary form must reproduce the above
 * copyright notice, this list of conditions and the following
 * disclaimer in the documentation and/or other materials
 * provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of
 * its contributors may be used to endorse or promote products
 * derived from this software without specific prior written
 * permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
 * CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
 * INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 * SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 * WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

#ifndef UBW_H
#define UBW_H
#include "GenericTypeDefs.h"
#include "Compiler.h"

#define kTX_BUF_SIZE           64u   // In bytes
#define kRX_BUF_SIZE          256u   // In bytes (defines maximum number of bytes in one command)
#define kRX_COMMAND_BUF_SIZE   64u   // In bytes (maximum number of bytes to pull from USB stack at a time)

#define kREQUIRED           FALSE
#define kOPTIONAL            TRUE

#define INPUT_PIN               1
#define OUTPUT_PIN              0

// These macros allow setting/clearing/testing a bit within a byte
// There are separate versions for dealing with bit zero because the compiler
// generates a warning if you try to shift the 1 zero bits to the left
#define bitset(var,bitno)   ((var) |= (1 << (bitno)))
#define bitsetzero(var)     ((var) |= 1)                      // Use this for setting bit zero of a byte
#define bitclr(var,bitno)   ((var) &= ~(1 << (bitno)))
#define bitclrzero(var)     ((var) &= ~1)                     // Use this for clearing bit zero of a byte
#define bittst(var,bitno)   (((var) & (1 << (bitno))) != 0u)  // Use this for testing bits 1 through 7 of a byte
#define bittstzero(var)     (((var) & 1) != 0u)               // Use this for testing bit zero of a byte


// Possible values for the variable error_byte
// Only one is allowed at once. This is a change in v3.0.2 (Issue #233)
// As soon as error_byte is non-zero, no other errors are recorded until the
// next command begins. Thus these are an enum which will fit into a byte,
// but unlike using bitfields will allow us to have more than 8 possible 
// errors.
typedef enum {
   kERROR_NO_ERROR = 0u
  ,kERROR_STEP_RATE_INVALID        // If you ask us to step more than 25 steps/ms
  ,kERROR_TX_BUF_OVERRUN
  ,kERROR_RX_BUFFER_OVERRUN
  ,kERROR_MISSING_PARAMETER
  ,kERROR_PRINTED_ERROR            // We've already printed out an error, so don't print anything else out in error parser
  ,kERROR_PARAMETER_OUTSIDE_LIMIT
  ,kERROR_EXTRA_CHARACTERS
  ,kERROR_CHECKSUM_NOT_FOUND_BUT_REQUIRED
} ErrorType;

// Enum for extract_num() function parameter
typedef enum {
   kCHAR          // One byte, signed
  ,kUCHAR         // One byte, unsigned
  ,kINT           // Two bytes, signed
  ,kUINT          // Two bytes, unsigned
  ,kASCII_CHAR    // ASCII character, read in as byte
  ,kUCASE_ASCII_CHAR  // ASCII character, must be uppercase
  ,kLONG          // Four bytes, signed
  ,kULONG         // Four bytes, unsigned
} ExtractType;

typedef enum {
   kEXTRACT_OK = 0
  ,kEXTRACT_PARAMETER_OUTSIDE_LIMIT
  ,kEXTRACT_COMMA_MISSING
  ,kEXTRACT_MISSING_PARAMETER
  ,kEXTRACT_INVALID_TYPE
  ,kEXTRACT_SKIPPING_BECAUSE_EXISTING_ERROR
} ExtractReturnType;

#define advance_RX_buf_out()          \
{                                     \
  g_RX_buf_out++;                     \
  if (kRX_BUF_SIZE == g_RX_buf_out)   \
  {                                   \
    g_RX_buf_out = 0;                 \
  }                                   \
}

// For the RC command, we define a little data structure that holds the 
// values associated with a particular servo connection
// It's port, pin, value (position) and state (INACTIVE, PRIMED or TIMING)
// Later on we make an array of these (19 elements long - 19 pins) to track
// the values of all of the servos.
typedef enum {
   kOFF = 1
  ,kWAITING
  ,kPRIMED
  ,kTIMING
} tRC_state;

// Use as the <type> parameters to the print_line_ending() call.
// These values only have meaning in "Legacy" mode, not in "New" mode.
typedef enum {
    kLE_OK_NORM
   ,kLE_NORM
   ,kLE_REV
} tLineEnding;

// States for the Stepper Disable Timeout feature
typedef enum {
    kSTEPPER_TIMEOUT_DISABLED   // Feature is not active and steppers won't disable
   ,kSTEPPER_TIMEOUT_PRIMED     // Feature active, motion is happening, waiting for motion stopped
   ,kSTEPPER_TIMEOUT_TIMING     // Counting down the seconds until time to disable steppers
   ,kSTEPPER_TIMEOUT_FIRED      // Timeout happened, steppers disabled
} tStepperDisableTimeout;

extern unsigned char g_RX_buf[kRX_BUF_SIZE];
extern unsigned char g_TX_buf_out;
extern volatile unsigned int ISR_A_FIFO[16];      // Stores the most recent analog conversions

extern ErrorType error_byte;
extern BOOL	g_ack_enable;

extern volatile unsigned long int gRCServoPoweroffCounterMS;
extern volatile unsigned long int gRCServoPoweroffCounterReloadMS;

extern volatile UINT8 near gRedLEDEmptyFIFO;
extern BOOL gAutomaticMotorEnable;
extern volatile UINT8 gLimitSwitchPortB;
extern volatile UINT8 gLimitSwitchReplies;
extern UINT8 gLimitSwitchReplyPrinted;

extern volatile UINT16 g_PowerMonitorThresholdADC;
extern volatile BOOL g_PowerDropDetected;

extern volatile UINT16 g_StepperDisableTimeoutS;
extern volatile UINT16 g_StepperDisableSecondCounter;
extern volatile UINT16 g_StepperDisableCountdownS;
extern volatile tStepperDisableTimeout g_StepperDisableState;  // Stores state of stepper timeout disable feature


/** P U B L I C  P R O T O T Y P E S *****************************************/
void print_stack(UINT8 tag);
void fill_stack(void);
void check_high_water(void);
void UserInit (void);
void ProcessIO (void);
void low_ISR (void);
void high_ISR (void);
ExtractReturnType extract_number (ExtractType Type, void * ReturnValue, unsigned char Required);
UINT8 extract_string (unsigned char * ReturnValue, UINT8 MaxBytes);
void print_command(BOOL print_always, BOOL print_comma);
void print_line_ending(tLineEnding);
void SetPinTRISFromRPn (char Pin, char State);
void SetPinLATFromRPn (char Pin, char State);
void AnalogConfigure (unsigned char Channel, unsigned char Enable);
void populateDeviceStringWithName(void);
int ebb_putc(char c);        // Our USB based stream character printer
void ErrorSet(ErrorType new_error);

#endif //UBW_H
