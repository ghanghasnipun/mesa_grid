import mesa_reader as mr
import numpy as np
import os
import subprocess

abs_path = f'/home/nipunghanghas/nipun_mesa/rgb_grid/' 
#abs_path = f'/homes/hanasoge/nipun_mesa/rgb_grid/' 
os.chdir(abs_path)

# m_range = np.round(np.arange(0.5,3,0.5),3)[:1]
# z_range = np.round(np.arange(0.001,0.05,0.01),3)[:1]
# e_range = np.round(np.arange(0.001,0.05,0.01),3)[:2]
# a = 2.2

m_range = np.array([3])
z_range = np.array([0.02])
e_range = np.array([0.02])
a = 2.2

def write_rg_inlist(m,z,e,a,l_dir):
    f = open("./inlist_to_start_he_core_flash","w")
    f.write(""" 
&star_job

      show_log_description_at_start = .false.
      create_pre_main_sequence_model = .true

      save_model_when_terminate = .false.
      save_model_filename = 'start_he_core_flash.mod'

      !required_termination_code_string = 'power_he_burn_upper_limit'
      required_termination_code_string = 'delta_nu_lower_limit'

      pgstar_flag = .true.

/ ! end of star_job namelist

&eos

/ ! end of eos namelist

&kap
      Zbase = 0.02d0

      kap_file_prefix = 'gs98'
      use_Type2_opacities = .true.

/ ! end of kap namelist

&controls

      power_he_burn_upper_limit = 10d0
      delta_nu_lower_limit = 2

      energy_eqn_option = 'eps_grav'
      use_gold2_tolerances = .true.
      time_delta_coeff = 1d0

      num_trace_history_values = 2
      trace_history_value_name(1) = 'rel_E_err'
      trace_history_value_name(2) = 'log_rel_run_E_err'

      ! limit max_model_number as part of test_suite
      max_model_number = 11000
         
      initial_mass = {}
      initial_z = {} 

      write_pulse_data_with_profile = .true.
      pulse_data_format = 'GYRE'


      ! mlt
      mixing_length_alpha = {}           !changing this
      use_Ledoux_criterion = .true.
      MLT_option = 'Henyey'
      
      
      ! mixing
      overshoot_scheme(1) = 'exponential'
      overshoot_zone_type(1) = 'any'
      overshoot_zone_loc(1) = 'any'
      overshoot_bdy_loc(1) = 'any'
      overshoot_f(1) =  {}             !changing this
      overshoot_f0(1) = 0.0001


      log_directory = '{}'
      photo_interval = 100
      profile_interval = 50
      history_interval = 10
      terminal_interval = 20
      write_header_frequency = 10

      !photo_interval = 1
      !profile_interval = 1
      !history_interval = 1
      !terminal_interval = 1

! FOR DEBUGGING

      !report_hydro_solver_progress = .true. ! set true to see info about solver iterations
      !report_ierr = .true. ! if true, produce terminal output when have some internal error
      !stop_for_bad_nums = .true.

      !hydro_get_a_numerical_partial = 1d-4
      !hydro_test_partials_k = 138
      !hydro_test_partials_call_number = 33
      !hydro_test_partials_iter_number = 11
      !hydro_test_partials_write_eos_call_info = .true.

/ ! end of controls namelist



&pgstar

         

         
      Grid6_win_flag = .true.
      Grid6_win_width = 11
         
      !Grid6_file_flag = .true.
      Grid6_file_dir = 'png'
      Grid6_file_prefix = 'grid6_'
      Grid6_file_interval = 5 ! output when mod(model_number,Grid6_file_interval)==0
      Grid6_file_width = -1 ! (inches) negative means use same value as for window
      Grid6_file_aspect_ratio = -1 ! negative means use same value as for window

      Summary_Burn_xaxis_name = 'mass' 
      Summary_Burn_xaxis_reversed = .false.
      Summary_Burn_xmin = 0.00 ! -101d0 ! only used if /= -101d0
      Summary_Burn_xmax = 2.1  ! only used if /= -101d0
      
      Abundance_xaxis_name = 'mass' 
      Abundance_xaxis_reversed = .false.
      ! power xaxis limits -- to override system default selections
      Abundance_xmin = 0.00 ! -101d0 ! only used if /= -101d0
      Abundance_xmax = -101d0 ! only used if /= -101d0
      Abundance_log_mass_frac_min = -6 ! only used if < 0

      !Profile_Panels4_win_flag = .true.
      !Profile_Panels4_win_width = 6
         
      ! Abundance window -- current model abundance profiles
      
         !Abundance_win_flag = .true.
      
         Abundance_win_width = 9
         Abundance_win_aspect_ratio = 0.75 ! aspect_ratio = height/width
   
/ ! end of pgstar namelist
""".format(m,z,a,e,l_dir))

def write_gyre_file(l_path,profile_num,min_freq,max_freq):
    f = open(l_path+"/gyre.in","w")
    f.write("""&constants
/

&model
  model_type = 'EVOL'  ! Obtain stellar structure from an evolutionary model
  file = '{}/profile{}.data.GYRE'    ! File name of the evolutionary model
  file_format = 'MESA' ! File format of the evolutionary model
/

&mode
  l = 1 ! Harmonic degree
/

&osc
  outer_bound = 'VACUUM' ! Assume the density vanishes at the stellar surface
/

&rot
/

&num
  diff_scheme = 'COLLOC_GL4' ! 4th-order collocation scheme for difference equations
/

&scan
  grid_type = 'LINEAR' ! Scan grid uniform in inverse frequency
  freq_min = {}        ! Minimum frequency to scan from
  freq_max = {}        ! Maximum frequency to scan to
  n_freq = 100          ! Number of frequency points in scan
  freq_units = 'UHZ'                   	      ! Units of freq output items
/

&grid
  w_osc = 10 ! Oscillatory region weight parameter
  w_exp = 2  ! Exponential region weight parameter
  w_ctr = 10 ! Central region weight parameter
/

""".format(l_path,profile_num,min_freq,max_freq))
    f.write("""
&ad_output
  summary_file_format = 'TXT'
  detail_file_format = 'TXT'
  summary_file = 'summary{}.txt'                         ! File name for summary file
  summary_item_list = 'l,n_pg,n_p,n_g,freq,freq_units,E_norm,E,E_p,E_g' ! Items to appear in summary file
  detail_template = 'profile{}.detail.l%l.n%n.txt'        	      ! File name template for detail files
  detail_item_list = 'l,n_pg,n_p,freq,freq_units,x,xi_r,
                      xi_h,c_1,As,V_2,Gamma_1' 	      ! Items to appear in detail files
  freq_units = 'UHZ'                   	      ! Units of freq output items
/

&nad_output
/

""".format(profile_num,profile_num))

for m_x in m_range:
    for z_x in z_range:
        for e_x in e_range:
            log_dir_local = f'RG_LOGS/{m_x}M{z_x}z{a}a{e_x}e'
            log_dir = abs_path+log_dir_local
            os.chdir(abs_path)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            write_rg_inlist(m_x,z_x,e_x,a,log_dir_local)
            print('Inlist written for logs dir : ',log_dir)
            # Add code to run the inlist
            subprocess.run(abs_path+'rn1',shell=True,check=True)
            print('\n\n MESA run complete!!')
            
            h = mr.MesaData(log_dir+'/history.data')
            l = mr.MesaLogDir(log_dir)
            select_model_number = h.model_number[(h.nu_max > 100)&(h.nu_max < 270)]
            select_profile_bool=(l.model_numbers>select_model_number[0])&(l.model_numbers<select_model_number[-1])
            req_profile_numbers,req_model_numbers=l.profile_numbers[select_profile_bool],l.model_numbers[select_profile_bool]
            l.profile_numbers[select_profile_bool],l.model_numbers[select_profile_bool]
            
            if req_model_numbers.shape[0]>0:
                for number in req_model_numbers:
                    number_profile = l.profile_with_model_number(number)
                    p = l.profile_data(model_number=number)
                    if p.model_number!=h.data_at_model_number('model_number',number):
                        print(p.model_number,h.data_at_model_number('model_number',number))
                        raise Exception('model_number in profile.data does not match with history.data')
                    print(p.model_number,h.data_at_model_number('nu_max',number),p.star_age)
                    min_freq = h.data_at_model_number('nu_max',number)-h.data_at_model_number('delta_nu',number)
                    max_freq = h.data_at_model_number('nu_max',number)+h.data_at_model_number('delta_nu',number)
                    write_gyre_file(log_dir,number_profile,min_freq,max_freq)
                    print('gyre file written at : ',log_dir,number_profile)
                    print('\nRunning GYRE on profile number : ',number_profile)
                    os.chdir(log_dir)
                    # Add code to run gyre
                    os.system(f'$GYRE_DIR/bin/gyre {log_dir}/gyre.in')
            else:
                print('No model satisfies the selection criteria.')
